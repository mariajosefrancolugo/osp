from django.conf import settings
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template

from osp.assessments.lib import jungian
from osp.assessments.models import PersonalityTypeResult, LearningStyleResult
from osp.core.middleware.http import Http403

def profile(request, username):
    if not request.user.groups.filter(
        name__in=['Students', 'Employees']):
        raise Http403

    student = User.objects.get(username__iexact=username)

    # Make sure the logged-in user should have access to this profile
    if (not request.user.groups.filter(name='Employees') and
        student != request.user):
        raise Http403

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

    return direct_to_template(request, 'profiles/profile.html', {
        'student': student,
        'current_enrollments': current_enrollments,
        'latest_ptr': latest_ptr,
        'pt_scores': pt_scores,
        'latest_lsr': latest_lsr,
    })
