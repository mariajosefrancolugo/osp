from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from osp.api.utils import check_credentials, load_users
from osp.core.models import UserProfile, Section, Enrollment

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
        stats = load_users(request.raw_post_data, ['Students'])

        status.append('Received %d student records' % stats[0])
        status.append('Updated %d user objects' % stats[1])
        status.append('Created %d user objects' % stats[2])
        status.append('Deactivated %d user accounts' % stats[3])
        status.append('Activated %d user accounts' % stats[4])
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_sections(request):
    status = ['Starting section import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Let's keep a count of how many new and updated objects we have
        sections_updated = 0
        sections_created = 0

        for s in data:
            # Finding (try) or creating (except) the section object
            try:
                section = Section.objects.get(prefix=s['prefix'],
                    number=s['number'], section=s['section'], term=s['term'],
                    year=s['year'])
                sections_updated += 1
            except:
                section = Section(prefix=s['prefix'], number=s['number'],
                    section=s['section'], term=s['term'], year=s['year'])
                sections_created += 1

            # Find the related instructor user object(s) for the section
            users = UserProfile.objects.filter(
                id_number__in=s['instructors'],
                user__groups__name='Instructors'
            )
            instructors = [u.user for u in users]

            # Update metadata for section
            section.title= s['title']
            section.credit_hours = s['credit_hours']

            # Save the section
            section.save()

            # Assign instructor user objects to section
            section.instructors.clear()
            [section.instructors.add(i) for i in instructors]

        status.append('Received %d section records' % len(data))
        status.append('Updated %d section objects' % sections_updated)
        status.append('Created %d section objects' % sections_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')

@csrf_exempt
def import_enrollments(request):
    status = ['Starting enrollment import...']

    if request.method == 'POST':
        # Check credentials and throw exception if invalid or non-existent
        check_credentials(request.META)

        # Convert JSON data to Python object
        data = json.loads(request.raw_post_data)

        # Let's keep a count of how many new and updated objects we have
        enrollments_updated = 0
        enrollments_created = 0

        # Start a cached list of courses
        sections = {}

        for e in data:
            # Find or create the enrollment object
            try:
                section = Section.objects.get(prefix=e['prefix'],
                    number=e['number'], section=e['section'], term=e['term'],
                    year=e['year'])
                student = UserProfile.objects.get(
                    id_number=e['student'],
                    user__groups__name='Students'
                ).user
                enrollment = Enrollment.objects.get(section=section,
                    student=student)
                enrollments_updated += 1
            except:
                # Find the related section object for the section
                #
                # We keep a cache that we check first, and then hit the DB
                # if we don't find it in the cache. If we don't find it in
                # the DB, we throw an exception.
                section_key = ('%s%s-%s-%s-%s' % (e['prefix'], e['number'],
                    e['section'], e['year'], e['term']))

                if (sections.has_key(section_key)):
                    section = sections[section_key]
                else:
                    try:
                        section = Section.objects.get(prefix=e['prefix'],
                            number=e['number'], section=e['section'],
                            term=e['term'], year=e['year'])
                        sections[section_key] = section
                    except:
                        raise Exception('Section %s does not exist' %
                            section_key)

                # Find the related student user object for the enrollment
                # Throw an exception if we can't find it
                try:
                    student = UserProfile.objects.get(
                        id_number=e['student'],
                        user__groups__name='Students'
                    ).user
                except:
                    raise Exception('Student %s does not exist' %
                        e['student'])

                enrollment = Enrollment(student=student, section=section)
                enrollments_created += 1


            # Ensure that metadata for enrollment is up-to-date
            enrollment.status = e['status']

            # This will need to change later
            enrollment.grade = 'N/A'

            enrollment.save()

        status.append('Received %d enrollment records' % len(data))
        status.append('Updated %d enrollment objects' % enrollments_updated)
        status.append('Created %d enrollment objects' % enrollments_created)
    else:
        status.append('Invalid request')

    return HttpResponse('\n'.join(status), mimetype='text/plain')
