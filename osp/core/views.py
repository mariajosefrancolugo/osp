import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.core.models import UserProfile
from osp.core.models import HelpTopic

@login_required
def index(request):
    if request.user.groups.filter(name='Employees'):
        return direct_to_template(request, 'core/index.html', {})
    elif request.user.groups.filter(name='Students'):
        return redirect('profile:profile', user_id=request.user.id)
    else:
        raise Http403

@login_required
def help(request):
    if not request.user.groups.filter(name='Employees'):
        raise Http403
    topics = []
    topics = HelpTopic.objects.all().order_by('order')
    return direct_to_template(request, 'core/help.html', { 'topics': topics })

@login_required
def search(request):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    term = request.GET.get('term', '')

    students = []
    if settings.INDEX_STUDENTS:
        from osp.core.models import StudentIndex

        if re.match(settings.ID_NUMBER_PATTERN, term):
            try:
                students = [StudentIndex.objects.filter(id_number=term)[0]]
            except IndexError:
                pass
        if not students:
            students = StudentIndex.objects.filter(
                Q(first_name__istartswith=term) |
                Q(last_name__istartswith=term) |
                Q(full_name__istartswith=term) |
                Q(email__istartswith=term)
            ).order_by('last_name', 'first_name').distinct()

        response = []
        for si in students:
            response.append({
                'value': si.full_name,
                'id': si.student.id,
                'desc': si.id_number,
            })
    else:
        if re.match(settings.ID_NUMBER_PATTERN, term):
            try:
                students = [UserProfile.objects.filter(
                    user__groups__name='Students', id_number=term
                )[0].user]
            except IndexError:
                pass
        if not students:
            # Ridiculously long query because we have to concatenate the first
            # and last name fields in order to filter on full name
            students = User.objects.filter(groups__name='Students').extra(
                where=["""(`auth_user`.`first_name` LIKE %s
                           OR `auth_user`.`last_name` LIKE %s
                           OR concat(`auth_user`.`first_name`, ' ',
                                     `auth_user`.`last_name`) LIKE %s
                           OR `auth_user`.`email` LIKE %s)"""],
                params=['%s%%' % term] * 4
            ).order_by('last_name', 'first_name').distinct()

        response = []
        for student in students:
            response.append({
                'value': '%s %s' % (student.first_name, student.last_name),
                'id': student.id,
                'desc': student.profile.id_number,
            })
    return HttpResponse(json.dumps(response), mimetype='application/json')
