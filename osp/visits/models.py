from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Visit(models.Model):
    student = models.ForeignKey(User, related_name='visits')
    submitter = models.ForeignKey(User, related_name='submitted_visits')
    campus = models.CharField(max_length=255, choices=settings.CAMPUS_CHOICES)
    contact_type = models.CharField(max_length=255,
                                    choices=settings.VISIT_CONTACT_TYPE_CHOICES)
    reason = models.CharField(max_length=255,
                              choices=settings.VISIT_REASON_CHOICES)
    department = models.CharField(max_length=255,
                                  choices=settings.VISIT_DEPARTMENT_CHOICES)
    undecided_financial_aid = models.BooleanField()
    career_services_outcome = models.CharField(
        max_length=255,
        choices=settings.VISIT_CAREER_SERVICES_OUTCOME_CHOICES,
        blank=True)
    note = models.TextField()
    private = models.BooleanField(help_text='Should be checked for visits '
                                            'that involve topics such as '
                                            'personal counseling')
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        ordering = ('-date_submitted',)
