from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403

@login_required
def index(request):
    if request.user.groups.filter(name='Employees'):
        return direct_to_template(request, 'core/index_employee.html', {})
    elif request.user.groups.filter(name='Students'):
        return direct_to_template(request, 'core/index_student.html', {})
    else:
        raise Http403

@login_required
def search(request):
    query = request.GET.get('term', '')

    # Ridiculously long query because we have to concatenate the first and
    # last name fields in order to filter on full name
    students = User.objects.filter(groups__name='Students').extra(
        where=[
            "(`auth_user`.`first_name` LIKE %s  OR `auth_user`.`last_name` "
            "LIKE %s OR concat(`auth_user`.`first_name`, ' ', "
            "`auth_user`.`last_name`) LIKE %s)"
        ],
        params=['%s%%' % query] * 3
    ).distinct()

    response = []
    for student in students:
        response.append({
            'value': '%s %s' % (student.first_name, student.last_name),
            'id': student.username
        })
    return HttpResponse(json.dumps(response), mimetype='application/json')
