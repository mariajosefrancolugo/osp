from django.conf.urls.defaults import *

from osp.api import views

urlpatterns = patterns('',
    (r'^instructors/import/', views.import_instructors, {},
        'import-instructors'),
    (r'^students/import/', views.import_students, {}, 'import-students'),
    (r'^courses/import/', views.import_courses, {}, 'import-courses'),
    (r'^sections/import/', views.import_sections, {}, 'import-sections'),
    (r'^enrollments/import/', views.import_enrollments, {},
        'import-enrollments'),
)
