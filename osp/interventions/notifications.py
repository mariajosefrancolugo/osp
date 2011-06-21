from django.conf import settings
from django.core.mail import EmailMessage

def email_user(from_user, to_user, subject, body):
    """Used to intercept emails when in debug mode"""
    if settings.DEBUG: # If it's not live
        subject = '(Orig: ' + to_user + ') ' + subject
        for debug_user in settings.DEBUG_USERS: # Send it to debug kids instead
            message = EmailMessage(
                subject, body, from_user, [debug_user[1]]
            )
            message.content_subtype = 'html'
            message.send()
        return "debug"
    else: # 
        message = EmailMessage(
            subject, body, from_user, [to_user]
        )
        message.content_subtype = 'html'
        message.send()
        return "live"
