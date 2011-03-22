import base64

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils import simplejson as json

def check_credentials(request_metadata):
    # Check for existence of credentials in request metadata
    if request_metadata.has_key('HTTP_AUTHORIZATION'):
        # Break down and decode provided credentials
        authorization = request_metadata['HTTP_AUTHORIZATION']
        authorization = authorization.replace('Basic ', '')
        credentials = base64.decodestring(authorization).split(':')

        # Check credentials against those stored in the app's settings
        if (credentials[0] != settings.API_USERNAME or
            credentials[1] != settings.API_PASSWORD):
            raise Exception('Invalid credentials')
    else:
        raise Exception('Missing credentials')

def load_users(raw_post_data, groups):
    # Convert JSON data to Python object
    data = json.loads(raw_post_data)

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
    for u in data:
        try:
            user = User.objects.get(username=u['username'])
            users_updated += 1
        except:
            user = User.objects.create_user(u['username'], u['email'])
            users_created += 1

        # Ensure that metadata for user is up-to-date
        user.first_name = u['first_name']
        user.last_name = u['last_name']
        user.email = u['email']

        # Make sure that user is in the appropriate groups
        for group in g:
            user.groups.add(group)

        # Adjust user's account status as necessary
        if user.is_active and not u['is_active']:
            user.is_active = False
            users_deactivated += 1
        elif not user.is_active and u['is_active']:
            user.is_active = True
            users_activated += 1

        user.save()

    # Return statistics on user account creation and modification
    return (len(data), users_updated, users_created, users_deactivated,
        users_activated)
