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

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Load users into local database using utility method
        stats = load_users(data, ['Instructors', 'Employees'])

        status.append('Received %d instructor records' % len(data))
        status.append('Updated %d user objects' % stats[0])
        status.append('Created %d user objects' % stats[1])
        status.append('Deactivated %d user accounts' % stats[2])
        status.append('Activated %d user accounts' % stats[3])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_students(request):
    status = ['Starting student import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Load users into local database using utility method
        stats = load_users(data, ['Students', 'Employees'])

        status.append('Received %d student records' % len(data))
        status.append('Updated %d user objects' % stats[0])
        status.append('Created %d user objects' % stats[1])
        status.append('Deactivated %d user accounts' % stats[2])
        status.append('Activated %d user accounts' % stats[3])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

def import_courses(request):
    pass

def import_sections(request):
    pass

def import_enrollments(request):
    pass
