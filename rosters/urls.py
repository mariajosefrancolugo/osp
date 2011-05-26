from django.conf.urls.defaults import *

from osp.rosters import views

urlpatterns = patterns('',
    (r'^(?P<section_id>\d+)/', views.roster, {}, 'roster'),
    (r'^submit/', views.submit_notification, {}, 'submit-notification'),
    (r'^compose/', views.compose_notification, {}, 'compose-notification'),
)
