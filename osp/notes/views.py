from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.views.generic.simple import direct_to_template
 
from osp.core.middleware.http import Http403
from osp.notes.models import Note
from osp.notes.forms import NoteForm

@login_required
def add_note(request, user_id):
    template = 'notes/add_note.html'

    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)

    if request.user.groups.filter(name='Counselors'):
        can_privatize = True
    else:
        can_privatize = False

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            note.submitter = request.user
            note.save()

            return HttpResponse(json.dumps({'status': 'success'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({
                'status': 'fail',
                'template': render_to_string(template, {
                'form': form,
                'student': student,
                'can_privatize': can_privatize}, RequestContext(request))
            }), content_type='application/json')
    else:
        form = NoteForm()

        return direct_to_template(request, template, {
            'form': form,
            'student': student,
            'can_privatize': can_privatize})

@login_required
def view(request, user_id, note_id):
    note = get_object_or_404(Note, id=note_id)
    if (not request.user.groups.filter(name='Employees')
        or (note.private
            and not request.user.groups.filter(name='Counselors'))):
        raise Http403

    return direct_to_template(request, 'notes/view.html', {
        'note': note})

@login_required
def view_all(request, user_id, page):
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)

    notes = Note.objects.filter(student=student)
    if not request.user.groups.filter(name='Counselors'):
        notes = notes.filter(private=False)

    page = int(page)
    paginator = Paginator(notes, 5)
    if page > paginator.num_pages:
        page = paginator.page(paginator.num_pages)
    elif page < 1:
        page = paginator.page(1)
    else:
        page = paginator.page(page)
    notes = page.object_list

    return direct_to_template(request, 'notes/view_all.html', {
        'notes': notes,
        'page': page,
        'paginator': paginator})


