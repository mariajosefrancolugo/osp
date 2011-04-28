def base_template(request):
    if request.user.groups.filter(name='Students'):
        return {'base_template': 'base_student.html'}
    elif request.user.groups.filter(name='Employees'):
        return {'base_template': 'base_employee.html'}
