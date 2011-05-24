from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from osp.core.models import Section
from osp.interventions.notifications import email_user

class Reason(models.Model):
    text = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.text

class Intervention(models.Model):
    students = models.ManyToManyField(User)
    reasons = models.ManyToManyField(Reason)
    date_submitted = models.DateTimeField(editable=False)
    campus = models.CharField(max_length=2, choices=settings.CAMPUS_CHOICES)
    staff = models.ForeignKey(User, related_name='intervention_staff')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    section = models.ForeignKey(Section)
    
    def save(self):
        if not self.id:
            self.date_submitted = datetime.today()
        super(Intervention, self).save()

    def email_intervention(self):
        # Send student emails letting them know
        message = "An intervention referral has been submitted on your behalf." #Need better message
        subject = "Intervention for %s %s: %s - %s" % (self.section.prefix, self.section.number, self.section.section, self.section.title)
        for student in self.students.all():
            if student.email:
                message = "%s,\n\n" % student.get_full_name() + message 
                email_user(student, subject, message)
        # Send email to settings.ALERT_REFERRAL_EMAIL
        email_user(self.staff, self.subject, self.message)
