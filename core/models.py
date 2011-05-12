from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gpa = models.FloatField(blank=True, null=True)

    def get_profile_url(self):
        return reverse('profile:profile', args=[self.user.username])

    def get_latest_personality_type_assessment_results(self):
        return self.user.personalitytyperesult_set.latest('date_taken')

    def get_latest_learning_style_assessment_results(self):
        return self.user.learningstyleresult_set.latest('date_taken')

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Section(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()
    instructors = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return '%s%s-%s' % (self.prefix, self.number, self.section)

    def get_active_enrollments(self):
        return self.enrollment_set.filter(status='A')


class Enrollment(models.Model):
    student = models.ForeignKey(User, blank=True, null=True)
    section = models.ForeignKey(Section)
    status = models.CharField(max_length=255,
        choices=settings.ENROLLMENT_STATUS_CHOICES)
    grade = models.CharField(max_length=255,
        choices=settings.ENROLLMENT_GRADE_CHOICES)
