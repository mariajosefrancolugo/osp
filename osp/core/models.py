from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    id_number = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_profile_url(self):
        return reverse('profile:profile', args=[self.user.id])

    def get_latest_pta_results(self):
        try:
            return self.user.personalitytyperesult_set.latest('date_taken')
        except:
            return None

    def get_latest_lsa_results(self):
        try:
            return self.user.learningstyleresult_set.latest('date_taken')
        except:
            return None

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Section(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()
    instructors = models.ManyToManyField(User)

    def __unicode__(self):
        return '%s%s-%s' % (self.prefix, self.number, self.section)

    def get_active_enrollments(self):
        from django.conf import settings
        return self.enrollment_set.filter(
            status__in=settings.ACTIVE_ENROLLMENT_STATUSES
        ).order_by('student__last_name')


class Enrollment(models.Model):
    student = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    status = models.CharField(max_length=255,
        choices=settings.ENROLLMENT_STATUS_CHOICES)

    def __unicode__(self):
        return '%s | %s | %s %d' % (self.section,
                                    self.student.username,
                                    self.section.term,
                                    self.section.year)
