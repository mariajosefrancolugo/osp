from django.conf.urls.defaults import *

from osp.visits import views

urlpatterns = patterns('',
    (r'^(?P<username>[\w.@+-]+)/page/(?P<page>[\d]+)/', views.visits, {}, 'visits'),
    (r'^(?P<username>[\w.@+-]+)/new/', views.submit_visit, {}, 'submit-visit'),
    (r'^(?P<username>[\w.@+-]+)/visit/(?P<visit_id>[\d]+)/', views.visit, {}, 'visit'),
)
