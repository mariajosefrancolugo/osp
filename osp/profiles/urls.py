from django.conf.urls.defaults import *

from osp.profiles import views

urlpatterns = patterns('',
    (r'^(?P<user_id>\d+)/', views.profile, {}, 'profile'),
    (r'^(?P<user_id>\d+)/all/(?P<page>\d+)/', views.view_all_activity, {}, 'view-all'),
)
