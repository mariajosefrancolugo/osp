from django.conf.urls.defaults import *

from osp.profiles import views

urlpatterns = patterns('',
    (r'^(?P<username>\w+)/', views.profile, {}, 'profile'),
)
