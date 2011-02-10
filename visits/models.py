from django.db import models
from django.contrib.auth.models import Group, User

class Visit(models.Model):
    author = models.ForeignKey(User, related_name='author_visits')
    student = models.ForeignKey(User, related_name='student_visits')
    notes = models.TextField()
    type = models.ForeignKey('VisitType')
    can_view = models.ManyToManyField(Group)

class VisitType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

