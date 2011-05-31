from django.contrib.auth.models import User, Group

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
        raise Exception("Missing host IP address")
    if host_received.strip() in authorized_hosts:
        if authorized_key != provided_key:
            print provided_key
            print authorized_key
            raise Exception("Invalid authorization key")
        return_status = True
    else:
        raise Exception("Unauthorized host IP address")
    return

def load_users(data, groups):
    # Store references to user groups
    g = Group.objects.filter(name__in=groups)

    # Let's keep a count of how many new and updated objects we have
    # Also, how many user accounts we activate or deactivate
    users_updated = 0
    users_created = 0

    # Grab all existing users and their associated objects in the
    # specified groups from the database
    all_users = UserProfile.objects.filter(
        user__groups__name__in=groups
    ).distinct().select_related()

    # Find or create user objects for each user
    for u in data:
        # Check if the user has a user account
        if u['username']:
            username = u['username']
            has_account = True
        # If the user does not have a user account, assign them a
        # temporary username based on their ID number
        else:
            if 'Students' in groups:
                username = str(u['id_number']) + 's'
            elif 'Employees' in groups:
                username = str(u['id_number']) + 'e'
            has_account = False

        # Get the existing user object or create a new one
        new_user = False
        try:
            user = all_users.filter(id_number=u['id_number'])[0].user
        except IndexError:
            user = User.objects.create_user(username, u['email'])
            new_user = True

        # Increment counter for appropriate operation type
        # Get or create the user profile object associated with the user
        if new_user:
            profile = UserProfile.objects.create(user=user)
            users_created += 1
        else:
            profile = all_users.filter(user=user)[0]
            users_updated += 1

        # Check if anything changed before updating the user object
        if (user.username != username
            or user.first_name != u['first_name']
            or user.last_name != u['last_name']
            or user.email != u['email']):
            user.username = username
            user.first_name = u['first_name']
            user.last_name = u['last_name']
            user.email = u['email']

            user.save()
        elif new_user:
            user.save()

        # Make sure that user is in the appropriate groups
        [user.groups.add(group)
         for group in g
         if group not in user.groups.all()]

        # Adjust user's account status as necessary
        if user.is_active and not u['is_active']:
            user.is_active = False
        elif not user.is_active and u['is_active']:
            user.is_active = True

        # Check if anything changed before updating the profile object
        if (profile.has_account != has_account
            or profile.id_number != u['id_number']
            or profile.phone_number != u['phone_number']):
            profile.has_account = has_account
            profile.id_number = u['id_number']
            profile.phone_number = u['phone_number']
            # profile.gpa = u['gpa']

            profile.save()

    # Return statistics on user account creation and modification
    return (len(data),
            users_updated,
            users_created)
