from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

BOOL_CHOICES = ((1, 'Private'), (0, 'Public'),(2, ''))
class Note(models.Model):
    students = models.ManyToManyField(User)
    submitter = models.ForeignKey(User, related_name='submitted_notes')
    note = models.TextField()
    private = models.BooleanField(default=2, choices=BOOL_CHOICES, help_text='Private should be checked for notes '
                                            'that involve topics such as '
                                            'personal counseling')
    date_submitted = models.DateTimeField(auto_now_add=True)


    class Meta(object):
        ordering = ('-date_submitted',)