from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from osp.api.utils import check_credentials, load_users
from osp.core.models import Course, Section, Enrollment

@csrf_exempt
def import_instructors(request):
    status = ['Starting instructor import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Load users into local database using utility method
        stats = load_users(request.raw_post_data, ['Instructors', 'Employees'])

        status.append('Received %d instructor records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        status.append('Deactivated %d user accounts' % stats[3])
        status.append('Activated %d user accounts' % stats[4])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_students(request):
    status = ['Starting student import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Load users into local database using utility method
        stats = load_users(request.raw_post_data, ['Students', 'Employees'])

        status.append('Received %d student records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        status.append('Deactivated %d user accounts' % stats[3])
        status.append('Activated %d user accounts' % stats[4])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_courses(request):
    status = ['Starting course import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Let's keep a count of how many new and updated objects we have
        # Also, how many user accounts we activate or deactivate
        courses_updated = 0
        courses_created = 0

        # Find or create course objects for each course
        for c in data:
            try:
                course = Course.objects.get(prefix=c['prefix'],
                    number=c['number'])
                courses_updated += 1
            except:
                course = Course(prefix=c['prefix'], number=c['number'])
                courses_created += 1

            # Ensure that metadata for course is up-to-date
            course.title= c['title']
            course.credit_hours = c['credit_hours']

            course.save()

        status.append('Received %d course records' % len(data))
        status.append('Updated %d course objects' % courses_updated)
        status.append('Created %d course objects' % courses_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_sections(request):
    status = ['Starting course import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Let's keep a count of how many new and updated objects we have
        # Also, how many user accounts we activate or deactivate
        courses_updated = 0
        courses_created = 0

        # Start a cached list of courses
        courses = []

        # Find the related course object for the section
        for s in data:
            try:
                course = Course.objects.get(prefix=c['prefix'],
                    number=c['number'])
                courses[course.prefix + course.number] = course
            except:
                course = Course(prefix=c['prefix'], number=c['number'])
                courses_created += 1

            # Ensure that metadata for course is up-to-date
            course.title= c['title']
            course.credit_hours = c['credit_hours']

            course.save()

        status.append('Received %d course records' % len(data))
        status.append('Updated %d course objects' % courses_updated)
        status.append('Created %d course objects' % courses_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_enrollments(request):
    pass
