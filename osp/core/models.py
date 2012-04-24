from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import simplejson as json

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    id_number = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    additional_data = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def deserialize_additional_data(self):
        """
           Value saved in additional_data is a json formatted string.
           Return it as a dictionary.

           Sample json format=
           [{"category":"SAT Results",
             "dataset":[{"groups_permitted":["Instructors","Counselors","Students"], "label":"Verbal", "value":600},
                        {"groups_permitted":["Counselors","Instructors","Students"], "label":"Math", "value":500},
                        {"groups_permitted":["Counselors", "Instructors","Students"], "label":"Essay", "value":9},
                        {"groups_permitted":["Instructors","Counselors","Students"], "label":"Total", "value":"1100"}]
            },
            {"category":"Test category 2",
             "dataset":[{"groups_permitted":["Instructors"], "label":"Field One", "value":"I am a test value for field one."},
                        {"groups_permitted":["Students"], "label":"Field Two", "value":"I am a test value for field two."},
                        {"groups_permitted":["Instructors", "Counselors"], "label":"Field Three", "value":"I am a test value for field three."}
            ]}]
        """
        return json.loads(self.additional_data)

    def permitted_additional_data(self,authenticated_user_groups):
        """
           Returns only the records from additional data that the authenticated user is
           permitted to view based on their group membership.
        """
        permitted_data=[]
        try:
            # Deserialize additional_data. 
            deserialized_data = self.deserialize_additional_data()
            for category in deserialized_data:
                return_dataset = []
                for record in category['dataset']:
                    # Cycle through the authenticated user's group membership
                    # to see if any match the groups permitted to view this record.
                    for group in authenticated_user_groups:
                        if group.name in record['groups_permitted']:
                           return_dataset.append(record)
                           break
                # If the authenticated user does not have permission to view any
                # of the records in the dataset for the current category, then
                # the category will not be included at all.
                if len(return_dataset) > 0:
                    permitted_data.append({"category":category['category'],
                                           "dataset":return_dataset})
        except:
            # If a problem occurs processing the information in the 
            # additional_data field, an empty list will be returned.
            pass
        return permitted_data
        

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
