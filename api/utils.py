from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import simplejson as json

from osp.core.models import UserProfile

def validate_credentials(request,
                         authorized_hosts,
                         authorized_key,
                         provided_key):
    if not provided_key:
        raise Exception('Missing authorization key')
    host_received = ''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        host_received = request.META['HTTP_X_FORWARDED_FOR']
    elif request.META.has_key('REMOTE_ADDR'):
        host_received = request.META['REMOTE_ADDR']
    else:
        raise Exception("Missing IP address")
    if host_received.strip() in authorized_hosts:
        if authorized_key != provided_key:
            print provided_key
            print authorized_key
            raise Exception("Invalid authorization key")
        return_status = True
    else:
        raise Exception("Unauthorized IP address")
    return

def load_users(request, user_type, groups):
    # Convert JSON data to Python object
    data = json.loads(request.raw_post_data)

    validate_credentials(request,
                         settings.API_ALLOWED_HOSTS,
                         settings.API_KEY,
                         data[0]['api_key'])

    # Store references to user groups
    g = []
    for group in groups:
        g.append(Group.objects.get(name=group))

    # Let's keep a count of how many new and updated objects we have
    # Also, how many user accounts we activate or deactivate
    users_updated = 0
    users_created = 0
    users_deactivated = 0
    users_activated = 0

    # Find or create user objects for each user
    for u in data[0][user_type]:
        if u['username']:
            username = u['username']
            has_account = True
        else:
            if 'Students' in groups:
                username = str(u['id_number']) + 's'
            elif 'Employees' in groups:
                username = str(u['id_number']) + 'e'
            has_account = False

        try:
            if 'Students' in groups:
                group = 'Students'
            elif 'Employees' in groups:
                group = 'Employees'

            user = UserProfile.objects.get(
                id_number=u['id_number'],
                user__groups__name=group
            ).user

            users_updated += 1
        except:
            user = User.objects.create_user(username, u['email'])
            users_created += 1

        # Ensure that metadata for user is up-to-date
        user.username = username
        user.first_name = u['first_name']
        user.last_name = u['last_name']
        user.email = u['email']

        # Make sure that user is in the appropriate groups
        user.groups.clear()
        for group in g:
            user.groups.add(group)

        # Adjust user's account status as necessary
        if user.is_active and not u['is_active']:
            user.is_active = False
            users_deactivated += 1
        elif not user.is_active and u['is_active']:
            user.is_active = True
            users_activated += 1

        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.has_account = has_account
        profile.id_number = u['id_number']
        profile.phone_number = u['phone_number']
        # profile.gpa = u['gpa']

        user.save()
        profile.save()

    # Return statistics on user account creation and modification
    return (len(data[0][user_type]),
            users_updated,
            users_created,
            users_deactivated,
            users_activated)
