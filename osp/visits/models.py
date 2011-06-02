from django.db import models
from django.contrib.auth.models import Group, User
from django.conf import settings
from datetime import datetime

class Visit(models.Model):
    student = models.ForeignKey(User, related_name='visit_students')
    campus = models.CharField(max_length=2, choices=settings.CAMPUS_CHOICES, help_text="")
    contact_type = models.CharField(max_length=2, choices=settings.VISIT_CONTACT_TYPE_CHOICES, help_text="")
    reason = models.CharField(max_length=4, choices=settings.VISIT_REASON_CHOICES, help_text="")
    department = models.CharField(max_length=2, choices=settings.VISIT_DEPARTMENT_CHOICES, help_text="")
    undecided_financial_aid = models.CharField(max_length=3, help_text="")
    career_services_outcome = models.CharField(max_length=2, choices=settings.VISIT_CAREER_SERVICES_OUTCOME_CHOICES, help_text="")  
    note = models.TextField(help_text="")
    submitter = models.ForeignKey(User, related_name='visit_submitters')
    date_submitted = models.DateTimeField(editable=False)
    private = models.BooleanField(default=False)

    def save(self):
        if not self.id:
            self.date_submitted = datetime.today()
        super(Visit, self).save()


