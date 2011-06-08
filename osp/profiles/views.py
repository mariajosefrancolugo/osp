from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.lib import jungian
from osp.core.middleware.http import Http403
from osp.visits.models import Visit

@login_required
def profile(request, user_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    student = get_object_or_404(User, pk=user_id, groups__name='Students')

    # Make sure the logged-in user should have access to this profile
    if (not request.user.groups.filter(name='Employees')
        and student != request.user):
        raise Http403

    current_enrollments = student.enrollment_set.filter(
        section__term=settings.CURRENT_TERM,
        section__year__exact=settings.CURRENT_YEAR)

    latest_pta_result = student.profile.get_latest_pta_results()
    latest_lsa_result = student.profile.get_latest_lsa_results()

    if latest_pta_result:
        pt_analysis = jungian.TypeAnalysis(
            args=json.loads(latest_pta_result.answers),
            likert=4,
            scale=100)
        pt_scores = [(s[0], s[1], (1 - s[1]))
                     for s in pt_analysis.graphScores]
    else:
        pt_scores = None

    visits = Visit.objects.filter(student=student)
    if (not request.user.groups.filter(name='Counselors')
        or not request.user.groups.filter(name='Instructors')):
        can_view_visits = False
    else:
        can_view_visits = True
    if not request.user.groups.filter(name='Counselors'):
        visits = visits.filter(private=False)
    if visits:
        paginator = Paginator(visits, 5)
        page = paginator.page(1)
        visits = page.object_list
    else:
        paginator = False
        page = False


    return direct_to_template(request, 'profiles/profile.html', {
        'student': student,
        'can_view_visits': can_view_visits,
        'current_enrollments': current_enrollments,
        'latest_pta_result': latest_pta_result,
        'pt_scores': pt_scores,
        'latest_lsa_result': latest_lsa_result,
        'visits': visits,
        'paginator': paginator,
        'page': page,
    })
