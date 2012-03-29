from django.conf.urls.defaults import *

from osp.notes import views

urlpatterns = patterns('',
    (r'^(?P<user_id>\d+)/all/(?P<page>\d+)/', views.view_all, {}, 'view-all'),
    (r'^(?P<user_id>\d+)/view/(?P<note_id>\d+)/', views.view, {}, 'view'),
    (r'^add/', views.add_note, {}, 'add_note'),
)

