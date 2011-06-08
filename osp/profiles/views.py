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

    latest_ptr = student.profile.get_latest_pta_results()
    latest_lsr = student.profile.get_latest_lsa_results()

    if latest_ptr:
        pt_analysis = jungian.TypeAnalysis(
            json.loads(latest_ptr.answers), 4, 100)
        pt_scores = []
        for score in pt_analysis.computedScores:
            pt_scores.append((score[0], score[1], (1 - score[1])))
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
        'latest_ptr': latest_ptr,
        'pt_scores': pt_scores,
        'latest_lsr': latest_lsr,
        'visits': visits,
        'paginator': paginator,
        'page': page,
    })
