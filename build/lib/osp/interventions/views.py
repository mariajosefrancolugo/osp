# from junk import stuff, things
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
# from django.utils import simplejson
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from osp.interventions.models import Intervention
from osp.interventions.forms import InterventionForm
from osp.core.models import Section
from osp.core.middleware.http import Http403


@login_required
def submit_intervention(request):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403
    
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.staff = request.user
            intervention.section = get_object_or_404(Section, id=request.POST['section_id'])
            intervention.message = newline_to_br(intervention.message)
            intervention.save()
            for student_id in request.POST['students'].split(','):
                intervention.students.add(get_object_or_404(User, id=int(student_id)))
            intervention.email_intervention()
            return HttpResponse('success')

    return HttpResponse('fail');

@login_required
def compose_intervention(request):
    if not request.user.groups.filter(name='Instructors'):
        raise Http403

    students = []
    if request.method == 'POST':
        section = get_object_or_404(Section, id=request.POST['section_id'])
        for student_id in request.POST.getlist('students'):
            students.append(get_object_or_404(User, id=int(student_id)))
        intervention = Intervention()
        intervention.message = render_to_string("interventions/email.html", {'students': students, 'staff': request.user })
        intervention.subject = "Interventions for %s - %s%s - %s" % (section.title, section.prefix, section.number, section.section)
        form = InterventionForm(instance=intervention)
        return direct_to_template(request, 'interventions/compose.html',
            {'form': form, 'students': students, 'section': section})
    else:
        return redirect('roster:roster', section_id=section.id)

def newline_to_br(text):
    return_text = ''
    for char in text:
        if char == '\n':
            return_text = return_text + '<br>'
        else:
            return_text = return_text + char
    return return_text
