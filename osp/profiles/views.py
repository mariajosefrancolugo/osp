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

class Activity:
    """
        Class used to create an Activity object.
    """
    def __init__(self, model, id, type, details, date_submitted, submitter, private):
        self.model = model
        self.id = id
        self.type = type
        self.details = details
        self.date_submitted = date_submitted
        self.submitter = submitter
        self.private = private

    def __repr__(self):
        return repr((self.model, self.id, self.type, self.details, self.date_submitted, self.submitter))

def get_activity(request, student_id, can_view_private):
    """
       Returns the combined activity (visits, notes, intervents, contacts 
       for the requested student.
    """
    from operator import attrgetter
    student = get_object_or_404(User, pk=student_id, groups__name='Students')
    if can_view_private:
        visits = student.visits.all()
        notes = student.note_set.all()
    else:
        visits = student.visits.filter(private=False)
        notes = student.note_set.filter(private=False)
    interventions = student.intervention_set.all()
    contacts = student.contact_set.all()
    combined_activity = []
    for visit in visits:
        combined_activity.append(Activity('visit',
                         visit.id,
                         'Visit - ' + visit.contact_type,
                         visit.reason,
                         visit.date_submitted,
                         visit.submitter,
                         visit.private))
    for note in notes:
        combined_activity.append(Activity('note',
                        note.id,
                        'Note',
                        note.note[:50],
                        note.date_submitted,
                        note.submitter,
                        note.private))
    for intervention in interventions:
        combined_activity.append(Activity('intervention',
                        intervention.id,
                        'Intervention',
                        intervention.reasons,
                        intervention.date_submitted,
                        intervention.instructor,
                        False))
    for contact in contacts:
        combined_activity.append(Activity('contact',
                        contact.id,
                        'Contact',
                        contact.message[:50],
                        contact.date_submitted,
                        contact.instructor,
                        False))
    activity = sorted(
        combined_activity,
        key=attrgetter('date_submitted'), reverse=True)
    return visits, notes, interventions, contacts, activity

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
        status__in=settings.ACTIVE_ENROLLMENT_STATUSES,
        section__term=settings.CURRENT_TERM,
        section__year__exact=settings.CURRENT_YEAR)

    try:
        latest_personality_type_result = (
            student.personalitytyperesult_set.latest('date_taken'))
    except:
        latest_personality_type_result = None
    try:
        latest_learning_style_result = (
            student.learningstyleresult_set.latest('date_taken'))
    except:
        latest_learning_style_result = None

    if latest_personality_type_result:
        personality_type_analysis = jungian.TypeAnalysis(
            args=json.loads(latest_personality_type_result.answers),
            likert=4,
            scale=100)
        personality_type_scores = [
            (score[0], score[1], (1 - score[1]))
            for score in personality_type_analysis.graphScores]
    else:
        personality_type_scores = None

    if (not request.user.groups.filter(name='Counselors')
        and not request.user.groups.filter(name='Instructors')):
        can_view_visits = False
        #visits = None
        activity = None
    else:
        can_view_visits = True
        #visits = Visit.objects.filter(student=student)
        can_view_private = True

        if not request.user.groups.filter(name='Counselors'):
            #visits = visits.filter(private=False)
            can_view_private = False
        visits, notes, interventions, contacts, activity = get_activity(request, student.id, can_view_private)

    #if visits:
    if activity:
        paginator = Paginator(activity, 5)
        page = paginator.page(1)
        activity = page.object_list
    else:
        paginator = False
        page = False

    return direct_to_template(request, 'profiles/profile.html', {
        'student': student,
        'current_enrollments': current_enrollments,
        'latest_personality_type_result': latest_personality_type_result,
        'personality_type_scores': personality_type_scores,
        'latest_learning_style_result': latest_learning_style_result,
        'can_view_visits': can_view_visits,
        'activity': activity,
        'paginator': paginator,
        'page': page,
    })

@login_required
def view_all_activity(request, user_id, page):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)

    #visits = Visit.objects.filter(student=student)
    #if not request.user.groups.filter(name='Counselors'):
    #    visits = visits.filter(private=False)
    
    can_view_private = True

    if not request.user.groups.filter(name='Counselors'):
        can_view_private = False
    visits, notes, interventions, contacts, activity = get_activity(request, student.id, can_view_private)


    page = int(page)
    paginator = Paginator(activity, 5)
    if page > paginator.num_pages:
        page = paginator.page(paginator.num_pages)
    elif page < 1:
        page = paginator.page(1)
    else:
        page = paginator.page(page)
    activity = page.object_list

    return direct_to_template(request, 'profiles/activity.html', {
        'activity': activity,
        'page': page,
        'paginator': paginator})
