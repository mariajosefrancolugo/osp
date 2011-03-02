from django.conf.urls.defaults import *

from osp.core import views

urlpatterns = patterns('',
    (r'^$', views.index, {}, 'index'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {}, 'logout'),
)
