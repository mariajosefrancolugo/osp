from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User, Group

from osp.rosters.models import Notification
from osp.rosters.forms import NotificationForm
from osp.interventions.views import newline_to_br
from osp.core.middleware.http import Http403
from osp.core.middleware.http import Http403
from osp.core.models import Section

@login_required
def roster(request, section_id):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    section = get_object_or_404(Section, id=section_id)

    if not section.instructors.filter(username=request.user.username):
        raise Http403

    # Calculate learning style totals for class
    ls_count = {'auditory': 0, 'kinesthetic': 0, 'visual': 0}
    for enrollment in section.get_active_enrollments():
        lsr = enrollment.student.profile.get_latest_lsa_results()
        if lsr:
            learning_styles = lsr.learning_style.split(', ')
            for ls in learning_styles:
                ls_count[ls] += 1

    return direct_to_template(request, 'rosters/roster.html',
        {'section': section, 'ls_count': ls_count})


@login_required
def submit_notification(request):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403
    
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.staff = request.user
            notification.section = get_object_or_404(Section, id=request.POST['section_id'])
            notification.message = newline_to_br(notification.message)
            notification.save()
            for student_id in request.POST['students'].split(','):
                notification.students.add(get_object_or_404(User, id=int(student_id)))
            notification.email_notification()
            return HttpResponse('success')

    return HttpResponse('fail');

@login_required
def compose_notification(request):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403

    students = []
    if request.method == 'POST':
        section = get_object_or_404(Section, id=request.POST['section_id'])
        for student_id in request.POST.getlist('students'):
            students.append(get_object_or_404(User, id=int(student_id)))
        notification = Notification()
        notification.subject = "Official Correspondence for %s %s: %s - %s" % (section.prefix, section.number, section.section, section.title)
        notification.message = "Dear Student,\n\n\nThanks,\n%s" % request.user.get_full_name()
        form = NotificationForm(instance=notification)
        return direct_to_template(request, 'rosters/compose.html',
            {'form': form, 'students': students, 'section': section})
    else:
        return redirect('roster:roster', section_id=section.id)
