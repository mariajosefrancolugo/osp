import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def email_user(user, subject, body):
    """Used to intercept emails when in debug mode"""
    if settings.DEBUG: # If it's not live
        for debug_user in settings.DEBUG_USERS: # Send it to debug kids instead
            subject = '(Orig: ' + user.email + ') ' + subject

            message = EmailMessage(
                subject, body, settings.ALERT_REFERRAL_EMAIL, [debug_user[1]]
            )
            message.content_subtype = 'html'
            message.send()
        return "debug"
    else: # 
        message = EmailMessage(
            subject, body, settings.ALERT_REFERRAL_EMAIL, [user.email]
        )
        message.content_subtype = 'html'
        message.send()
        return "live"
