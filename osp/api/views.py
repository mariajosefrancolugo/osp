from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from osp.api.utils import (validate_credentials,
                           get_existing_users,
                           get_existing_sections,
                           get_existing_enrollments,
                           load_users)
from osp.core.models import UserProfile, Section, Enrollment

@csrf_exempt
def import_instructors(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0]['api_key'])

        # Load users into local database using utility method
        stats = load_users(data[0]['instructors'], ['Instructors', 'Employees'])
        status.append('Received %d instructor records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        if len(stats[3]) > 0:
           status.append('Instructor records in error:')
           for item in stats[3]:
               status.append(item)
        if len(stats[4]) > 0:
           status.append('Instructor records with improperly formatted json string in additional_data:')
           for item in stats[4]:
               status.append(item)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_counselors(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0]['api_key'])

        # Load users into local database using utility method
        stats = load_users(data[0]['counselors'], ['Counselors', 'Employees'])

        status.append('Received %d counselor records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        if len(stats[3]) > 0:
           status.append('Counselor records in error:')
           for item in stats[3]:
               status.append(item)
        if len(stats[4]) > 0:
           status.append('Counselor records with improperly formatted json string in additional_data:')
           for item in stats[4]:
               status.append(item)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_students(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0]['api_key'])

        # Load users into local database using utility method
        stats = load_users(data[0]['students'], ['Students'])

        status.append('Received %d student records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        if len(stats[3]) > 0:
           status.append('Student records in error:')
           for item in stats[3]:
               status.append(item)
        if len(stats[4]) > 0:
           status.append('Student records with improperly formatted json string in additional_data:')
           for item in stats[4]:
               status.append(item)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_sections(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0].get('api_key', ''))

        # Redefine data variable to the actual section list
        data = data[0]['sections']

        # Let's keep a count of how many new and updated objects we have
        sections_updated = 0
        sections_created = 0

        # Grab all existing sections and users as well as their associated
        # objects from the database
        existing_sections = get_existing_sections(settings.CURRENT_TERM,
                                                  settings.CURRENT_YEAR)

        id_numbers = []
        for s in data:
            for i in s['instructors']:
                id_numbers.append(i)

        existing_users = get_existing_users(['Instructors'], id_numbers)

        for s in data:
            # Get the existing section object or create a new one
            key = '%s%s-%s-%s-%d' % (s['prefix'],
                                     s['number'],
                                     s['section'],
                                     s['term'],
                                     int(s['year']))
            section = existing_sections.get(key)

            new_section = False
            if not section:
                section = Section(prefix=s['prefix'],
                                  number=s['number'],
                                  section=s['section'],
                                  term=s['term'],
                                  year=s['year'])
                new_section = True

            # Increment counter for appropriate operation type
            if new_section:
                sections_created += 1
            else:
                sections_updated += 1

            # Only update metadata for section if changed
            if (section.title != s['title']
                or section.credit_hours != s['credit_hours']):
                section.title= s['title']
                section.credit_hours = s['credit_hours']

                section.save()
            elif new_section:
                section.save()

            # Clear existing instructors and add up-to-date list of
            # instructors to section
            section.instructors.clear()
            for i in s['instructors']:
                instructor = existing_users.get(i)

                instructor_exists = True
                if not instructor:
                    status.append('Instructor (ID number %s) '
                                  'does not exist' % i)
                    instructor_exists = False

                if instructor_exists:
                    section.instructors.add(instructor)


        status.append('Received %d section records' % len(data))
        status.append('Updated %d section objects' % sections_updated)
        status.append('Created %d section objects' % sections_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_enrollments(request):
    status = []
    if request.method == 'POST':
        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        validate_credentials(request,
                             settings.API_ALLOWED_HOSTS,
                             settings.API_KEY,
                             data[0].get('api_key', ''))

        # Redefine data variable to actual enrollment list
        data = data[0]['enrollments']

        # Let's keep a count of how many new and updated objects we have
        enrollments_updated = 0
        enrollments_created = 0

        # Grab all existing sections, users, and enrollments as well as
        # their associated objects from the database
        existing_sections = get_existing_sections(settings.CURRENT_TERM,
                                                  settings.CURRENT_YEAR)

        id_numbers = []
        for e in data:
            id_numbers.append(e['student'])

        existing_users = get_existing_users(['Students'], id_numbers)
        existing_enrollments = get_existing_enrollments(settings.CURRENT_TERM,
                                                        settings.CURRENT_YEAR)

        for e in data:
            key = '%s%s-%s-%s-%d' % (e['prefix'],
                                     e['number'],
                                     e['section'],
                                     e['term'],
                                     int(e['year']))
            section = existing_sections.get(key)

            section_exists = True
            if not section:
                status.append('Section (%s%s-%s) does not exist' % (
                    e['prefix'],
                    e['number'],
                    e['section']))
                section_exists = False

            student = existing_users.get(e['student'])

            student_exists = True
            if not student:
                status.append('Student (ID number %s) '
                              'does not exist' % e['student'])
                student_exists = False

            if section_exists and student_exists:
                key = '%s-%s%s-%s-%s-%d' % (e['student'],
                                            e['prefix'],
                                            e['number'],
                                            e['section'],
                                            e['term'],
                                            int(e['year']))
                enrollment = existing_enrollments.get(key)

                new_enrollment = False
                if not enrollment:
                    enrollment = Enrollment(student=student, section=section)
                    new_enrollment = True

                if new_enrollment:
                    enrollments_created += 1
                else:
                    enrollments_updated += 1


                # Only update metadata for enrollment if changed
                if enrollment.status != e['status']:
                    enrollment.status = e['status']
                    enrollment.save()
                elif new_enrollment:
                    enrollment.save()

        status.append('Received %d enrollment records' % len(data))
        status.append('Updated %d enrollment objects' % enrollments_updated)
        status.append('Created %d enrollment objects' % enrollments_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')
