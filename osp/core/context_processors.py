from django.conf import settings

def media_url(request):
    return {'MEDIA_URL': settings.MEDIA_URL}

def base_template(request):
    if request.user.groups.filter(name='Employees'):
        return {'base_template': 'base_employee.html'}
    elif request.user.groups.filter(name='Students'):
        return {'base_template': 'base_student.html'}
    else:
        return {'base_template': 'base.html'}

def classes(request):
    if request.user.groups.filter(name='Instructors'):
        sections = request.user.section_set.filter(term=settings.CURRENT_TERM,
                                                   year=settings.CURRENT_YEAR)
        return {'classes': sections}
    else:
        return {'classes': None}

def assessments(request):
    try:
        custom_assessments = settings.CUSTOM_ASSESSMENTS
    except:
        custom_assessments = []
    return {'CUSTOM_ASSESSMENTS': custom_assessments}
