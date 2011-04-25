from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.lib import jungian
from osp.assessments.models import PersonalityTypeResult, LearningStyleResult

def profile(request, username):
    if not request.user.groups.filter(
        name__in=['Students', 'Employees']):
        return HttpResponseForbidden()

    student = User.objects.get(username__iexact=username)

    # Make sure the logged-in user should have access to this profile
    if (not request.user.groups.filter(name='Employees') and
        student != request.user):
        return HttpResponseForbidden()

    current_enrollments = student.enrollment_set.filter(
        section__term=settings.CURRENT_TERM,
        section__year__exact=settings.CURRENT_YEAR
    )

    latest_ptr = None
    pt_scores = None
    latest_lsr = None
    try:
        latest_ptr = student.personalitytyperesult_set.latest('date_taken')
        pt_analysis = jungian.TypeAnalysis(
            json.loads(latest_ptr.answers), 4, 100)
        pt_scores = []
        for score in pt_analysis.computedScores:
            pt_scores.append((score[0], score[1], (1 - score[1])))
        latest_lsr = student.learningstyleresult_set.latest('date_taken')
    except PersonalityTypeResult.DoesNotExist, LearningStyleResult.DoesNotExist:
        pass

    if request.user.groups.filter(name='Students'):
        base_template = 'base_student.html'
    elif request.user.groups.filter(name='Employees'):
        base_template = 'base_employee.html'

    return direct_to_template(request, 'profiles/profile.html', {
        'student': student,
        'current_enrollments': current_enrollments,
        'latest_ptr': latest_ptr,
        'pt_scores': pt_scores,
        'latest_lsr': latest_lsr,
        'base_template': base_template
    })
