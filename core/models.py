from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()


class Section(models.Model):
    course = models.ForeignKey(Course)
    instructor = models.ForeignKey(User)
    term = models.CharField(max_length=255)
    year = models.IntegerField()


class Enrollment(models.Model):
    student = models.ForeignKey(User)
    section = models.ForeignKey(Section)
