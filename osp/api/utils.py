import sys

from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.utils import simplejson as json

from osp.core.models import UserProfile, Section, Enrollment

def validate_credentials(request, authorized_hosts, valid_key, provided_key):
    if not provided_key:
        raise Exception('Missing authorization key')

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        host_received = request.META['HTTP_X_FORWARDED_FOR']
    elif request.META.has_key('REMOTE_ADDR'):
        host_received = request.META['REMOTE_ADDR']
    else:
        raise Exception("Missing host IP address")

    if host_received.strip() in authorized_hosts:
        if valid_key != provided_key:
            raise Exception("Invalid authorization key")
    else:
        raise Exception("Unauthorized host IP address")

    return

def get_existing_users(groups, id_numbers):
    user_profiles = UserProfile.objects.filter(
        id_number__in=id_numbers,
        user__groups__name__in=groups
    ).distinct().select_related()

    existing_users = {}
    for user_profile in user_profiles:
        existing_users[user_profile.id_number] = user_profile.user

    return existing_users

def get_existing_sections(term, year):
    sections = Section.objects.filter(term=term, year=year).select_related()

    existing_sections = {}
    for section in sections:
        key = '%s%s-%s-%s-%d' % (section.prefix,
                                 section.number,
                                 section.section,
                                 section.term,
                                 section.year)
        existing_sections[key] = section

    return existing_sections

def get_existing_enrollments(term, year):
    enrollments = Enrollment.objects.filter(
        section__term=term, section__year__exact=int(year)
    ).select_related()

    existing_enrollments = {}
    for enrollment in enrollments:
        key = '%s-%s%s-%s-%s-%d' % (enrollment.student.profile.id_number,
                                    enrollment.section.prefix,
                                    enrollment.section.number,
                                    enrollment.section.section,
                                    enrollment.section.term,
                                    enrollment.section.year)
        existing_enrollments[key] = enrollment

    return existing_enrollments

def load_users(data, groups):
    # Store references to user groups
    g = Group.objects.filter(name__in=groups)
    group_objs = []
    for group in g:
        group_objs.append(group)

    # Let's keep a count of how many new and updated objects we have
    # Also, how many user accounts we activate or deactivate
    # And, a list of user records that threw exceptions and therefore
    # were not properly saved.
    users_updated = 0
    users_created = 0
    user_exceptions = []
    additional_data_exceptions = []

    id_numbers = []
    for u in data:
        id_numbers.append(u['id_number'])

    # Grab all existing users and their associated objects in the
    # specified groups from the database
    existing_users = get_existing_users(groups, id_numbers)

    # Find or create user objects for each user
    for u in data:
        try:
            # Check if the user has a user account
            if u['username']:
                username = u['username']
            # If the user does not have a user account, assign them a
            # temporary username based on their ID number
            else:
                if 'Students' in groups:
                    username = '%ss' % u['id_number']
                elif 'Employees' in groups:
                    username = '%se' % u['id_number']

            # Get the existing user object or create a new one
            user = existing_users.get(u['id_number'])

            new_user = False
            if not user:
                try:
                    user = User.objects.create_user(username, u['email'])
                    new_user = True
                except IntegrityError, (errno, strerror):
                    # If the user record already exists and just isn't in
                    # the correct group (and therefore not in the queryset
                    # we pulled earlier), grab it
                    # MySQL error # 1062 = duplicate entry
                    if errno == 1062:
                        user = User.objects.get(username=username)

            # Increment counter for appropriate operation type
            # Get or create the user profile object associated with the user
            if new_user:
                profile = UserProfile.objects.create(user=user)
                users_created += 1
            else:
                profile = user.profile
                users_updated += 1

            # Check if anything changed before updating the user object
            if (user.username != username
                or user.first_name != u['first_name']
                or user.last_name != u['last_name']
                or user.email != u['email']
                or user.is_active != u['is_active']):
                user.username = username
                user.first_name = u['first_name']
                user.last_name = u['last_name']
                user.email = u['email']
                user.is_active = u['is_active']

                user.save()
            elif new_user:
                user.save()

            group_memberships = []
            for group in user.groups.all():
                group_memberships.append(group)

            # Make sure that user is in the appropriate groups
            [user.groups.add(group)
             for group in group_objs
             if group not in group_memberships]

            # Check if anything changed before updating the profile object
            if (profile.id_number != u['id_number']
                or profile.phone_number != u['phone_number']
                or ('additional_data' in u and profile.additional_data != u['additional_data'])):
                profile.id_number = u['id_number']
                profile.phone_number = u['phone_number']
                if 'additional_data' in u:
                    try:
                        # convert additional_data back into a json formatted string to save
                        profile.additional_data = json.dumps(u['additional_data'])
                    except:
                        # if additional_data contained improperly formatted json, an error should
                        # have been triggered before now
                        additional_data_exceptions.append('Invalid json format in additional_data: %s' % u)
                profile.save()
        except:
            user_exceptions.append('%s %s' % (sys.exc_info()[0], u))
    # Return statistics on user account creation and modification
    return (len(data), users_updated, users_created, user_exceptions, additional_data_exceptions)
