from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template

@login_required
def index(request):
    if request.user.groups.filter(name='Employees'):
        return direct_to_template(request, 'core/index_employee.html', {})
    elif request.user.groups.filter(name='Students'):
        return direct_to_template(request, 'core/index_student.html', {})
