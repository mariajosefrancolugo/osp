from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    id_number = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    additional_data = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class StudentIndex(models.Model):
    student = models.OneToOneField(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=61)
    email = models.CharField(max_length=75)
    id_number = models.CharField(max_length=255)

    def __unicode__(self):
        return self.student.username

if settings.INDEX_STUDENTS:
    from osp.core.signals import update_index
    post_save.connect(update_index, sender=User)


class Section(models.Model):
    prefix = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    credit_hours = models.FloatField()
    instructors = models.ManyToManyField(User)

    class Meta(object):
        ordering = ('prefix', 'number', 'section',)

    def __unicode__(self):
        return '%s%s-%s' % (self.prefix, self.number, self.section)

    def get_active_enrollments(self):
        from django.conf import settings
        return self.enrollment_set.filter(
            status__in=settings.ACTIVE_ENROLLMENT_STATUSES
        ).order_by('student__last_name', 'student__first_name')


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
