import traceback

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from osp.api.utils import check_credentials
from osp.core.models import Course, Section, Enrollment


@csrf_exempt
def import_instructors(request):
    status = ['Starting instructor import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python dictionary
        data = json.loads(request.raw_post_data)

        # Store reference to Instructors and Employees user groups
        instructors_group = Group.objects.get(name='Instructors')
        employees_group = Group.objects.get(name='Employees')

        # Let's keep a count of how many new and updated objects we have
        # Also, how many user accounts we activate or deactivate
        users_updated = 0
        users_created = 0
        users_deactivated = 0
        users_activated = 0

        # Find or create user objects for each instructor
        for instructor in data:
            try:
                user = User.objects.get(username=instructor['username'])
                users_updated += 1
            except:
                user = User.objects.create_user(instructor['username'],
                    instructor['email'])
                users_created += 1

            # Ensure that metadata for user is up-to-date
            user.first_name = instructor['first_name']
            user.last_name = instructor['last_name']
            user.email = instructor['email']

            # Make sure that user is in the appropriate groups
            user.groups.add(instructors_group)
            user.groups.add(employees_group)

            # Adjust user's account status as necessary
            if user.is_active and not instructor['is_active']:
                user.is_active = False
                users_deactivated += 1
            elif not user.is_active and instructor['is_active']:
                user.is_active = True
                users_activated += 1

            user.save()

        status.append('Received %d instructor records' % len(data))
        status.append('Updated %d user objects' % users_updated)
        status.append('Created %d user objects' % users_created)
        status.append('Deactivated %d user accounts' % users_deactivated)
        status.append('Activated %d user accounts' % users_activated)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

def import_students(request):
    pass

def import_courses(request):
    pass

def import_sections(request):
    pass

def import_enrollments(request):
    pass
