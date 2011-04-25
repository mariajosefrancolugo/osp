from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gpa = models.FloatField()


class StudentGroup(models.Model):
    owner = models.ForeignKey(User, related_name='owned_student_groups')
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User,
        related_name='student_group_memberships')


class Course(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()


class Section(models.Model):
    course = models.ForeignKey(Course)
    section = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    year = models.IntegerField()
    instructor = models.ForeignKey(User)


STATUS_CHOICES = (
    ('A', 'Active'),
    ('DFNP', 'Dropped for Non-Payment'),
    ('DBS', 'Dropped by Student'),
    ('DBI', 'Dropped by Instructor'),
    ('C', 'Complete'),
)

GRADE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('F', 'F'),
    ('W', 'W'),
)

class Enrollment(models.Model):
    student = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
