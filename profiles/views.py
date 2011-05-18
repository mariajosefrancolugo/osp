from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator

from osp.assessments.lib import jungian
from osp.core.middleware.http import Http403
from osp.visit.models import Visit

@login_required
def profile(request, user_id):
    if not request.user.groups.filter(name__in=['Students', 'Employees']):
        raise Http403

    student = User.objects.get(pk=user_id)

    # Make sure the logged-in user should have access to this profile
    if (not request.user.groups.filter(name='Employees') and
        student != request.user):
        raise Http403

    current_enrollments = student.enrollment_set.filter(
        section__term=settings.CURRENT_TERM,
        section__year__exact=settings.CURRENT_YEAR
    )

    try:
        latest_ptr = student.personalitytyperesult_set.latest('date_taken')
    except:
        latest_ptr = None
    try:
        latest_lsr = student.learningstyleresult_set.latest('date_taken')
    except:
        latest_lsr = None

    if latest_ptr:
        pt_analysis = jungian.TypeAnalysis(
            json.loads(latest_ptr.answers), 4, 100)
        pt_scores = []
        for score in pt_analysis.computedScores:
            pt_scores.append((score[0], score[1], (1 - score[1])))
    else:
        pt_scores = None

    visits = Visit.objects.filter(student=student)
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
        'current_enrollments': current_enrollments,
        'latest_ptr': latest_ptr,
        'pt_scores': pt_scores,
        'latest_lsr': latest_lsr,
        'visits': visits,
        'paginator': paginator,
        'page': page,
    })
