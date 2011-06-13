from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template

from osp.core.middleware.http import Http403
from osp.visits.models import Visit
from osp.visits.forms import VisitForm

@login_required
def submit_visit(request, user_id):
    """
        Check permissions before doing anything and point people to the door
        as needed. For those so allowed, return a blank form.
        If the form submitted is invalid, return the form again, filled in both
        with the data from the user and the pertinent errors.
        Finally, when the form is successfully and authoritatively submitted,
        return some kind of confirmation.
    """
    if not request.user.groups.filter(name='Employees'):
        raise Http403

    student = get_object_or_404(User, id=user_id)
    if request.user.groups.filter(name='Counselors'):
        can_privatize = True
    else:
        can_privatize = False

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.student = student
            visit.submitter = request.user
            visit.save()
            return redirect('visit:visit',
                            user_id=student.id,
                            visit_id=visit.id)

    else:
        form = VisitForm()

    return direct_to_template(request, 'visits/visit.html', {
        'form': form,
        'student': student,
        'can_privatize': can_privatize})

@login_required
def visit(request, user_id, visit_id):
    """
        Check permissions before doing anything, and point people to the door
        as needed. For those so allowed, return a view of the visit.
    """
    visit = get_object_or_404(Visit, id=visit_id)
    student = get_object_or_404(User, id=user_id)
    if (not request.user.groups.filter(name='Employees')
        or (visit.private
            and not request.user.groups.filter(name='Counselors'))):
        raise Http403

    return direct_to_template(request, 'visits/visit_detail.html', {
        'visit': visit,
        'student': student})

@login_required
def visits(request, user_id, page):
    """
        Check permissions before doing anything, and point people to the door
        as needed. I'm a broken record. For those so allowed, return all the
        visits for a specific student.
    """
    if not request.user.groups.filter(name='Employees'):
        raise Http403
    student = get_object_or_404(User, id=user_id)
    visits = Visit.objects.filter(student=student)
    if not request.user.groups.filter(name='Counselors'):
        visits = visits.filter(private=False)

    page = int(page)
    paginator = Paginator(visits, 5)
    if page > paginator.num_pages:
        page = paginator.page(paginator.num_pages)
    elif page < 1:
        page = paginator.page(1)
    else:
        page = paginator.page(page)
    visits = page.object_list

    return direct_to_template(request, 'visits/visits.html', {
        'visits': visits,
        'page': page,
        'paginator': paginator,
        'student': student})
