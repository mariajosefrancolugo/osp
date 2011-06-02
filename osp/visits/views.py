# from junk import stuff, things
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
# from django.utils import simplejson
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from osp.visits.models import Visit
from osp.visits.forms import VisitForm
from osp.core.middleware.http import Http403


# TODO: Create view to serve empty form, serve error'd form, and save valid form
#       and redirect to the visit itself OR show as submitted.
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
        post = request.POST.copy()
        post['student'] = student.id
        post['submitter'] = request.user.id
        form = VisitForm(post)
        if form.is_valid():
            print "Yep"
            visit = form.save()
            return redirect('visit:visit',
                user_id=student.id,
                visit_id=visit.id)
        print form.errors
    else:
        form = VisitForm()

    return direct_to_template(request, 'visits/visit.html',
        {'form': form, 'student': student, 'can_privatize': can_privatize})


# TODO: Create view to show individual visit information.
@login_required
def visit(request, user_id, visit_id):
    """
        Check permissions before doing anything, and point people to the door
        as needed. For those so allowed, return a view of the visit.
    """
    visit = get_object_or_404(Visit, id=visit_id)
    student = get_object_or_404(User, id=user_id)
    if not request.user.groups.filter(name='Employees') or (visit.private and not request.user.groups.filter(name='Counselors')):
        raise Http403
    
    return direct_to_template(request, 'visits/visit_detail.html',
        {'visit': visit, 'student': student}) 


# TODO: Create method to return all visits? Some method of permissioning and
#       returning some meaningful message in the case of lack of permission.
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
    
    return direct_to_template(request, 'visits/visits.html',
        {'visits': visits, 'page': page, 'paginator': paginator, 'student': student})

# TASKS:
# A) Faculty and staff can submit information related to a student visit
#    i.   Done in submit_visit
#    ii.  Should check for permission to create visit and handle lack of
#         permissions gracefully and informatively
#    iii. Should handle invalid form submission informatively.
#    iv.  Upon successful form submission, redirect to either
#         a.  The visit view
#         b.  A simple message stating the successful submission
#
# B) Visits for a student can be viewed by staff on student profile
#    i.   Done in visit and visits
#    ii.  Should check for permissions on both and handle lack of permissions
#         gracefully and informatively.
#    iii. Should not even show links or references to visits if the user is not
#         permitted to view them in detail?
