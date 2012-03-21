from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Note(models.Model):
    student = models.ForeignKey(User, related_name='notes')
    submitter = models.ForeignKey(User, related_name='submitted_notes')
    note = models.TextField()
    private = models.BooleanField(help_text='Should be checked for notes '
                                            'that involve topics such as '
                                            'personal counseling')
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        ordering = ('-date_submitted',)
