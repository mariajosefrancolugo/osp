from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from osp.core.models import Section
from osp.interventions.notifications import email_user

class Notification(models.Model):
    students = models.ManyToManyField(User)
    date_submitted = models.DateTimeField(editable=False)
    staff = models.ForeignKey(User, related_name='notifications_staff')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    section = models.ForeignKey(Section)

    def save(self):
        if not self.id:
            self.date_submitted = datetime.today()
        super(Notification, self).save()

    def email_notification(self):
        # Send student emails letting them know
        for student in self.students.all():
            if student.email:
                email_user(settings.OSP_EMAIL,
                           student.email,
                           self.subject,
                           self.message)
