from django.conf.urls.defaults import *

from osp.reports import views

urlpatterns = patterns('',
    (r'^learning-style/', views.learning_style_report, {},
        'learning-style-report'),
    (r'^personality-type/', views.personality_type_report, {},
        'personality-type-report'),
    (r'^visit/', views.visit_report, {}, 'visit-report'),
)
