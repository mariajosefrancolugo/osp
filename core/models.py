from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gpa = models.FloatField()


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class StudentGroup(models.Model):
    owner = models.ForeignKey(User, related_name='owned_student_groups')
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User,
        related_name='student_group_memberships')


class Section(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()
    instructors = models.ManyToManyField(User)


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
    ('I', 'I'),
    ('N/A', 'N/A'),
)

class Enrollment(models.Model):
    student = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES)
