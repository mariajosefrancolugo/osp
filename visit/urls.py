from django.conf.urls.defaults import *
from osp.visit import views

urlpatterns = patterns('',
    (r'^(?P<user_id>[\w.@+-]+)/page/(?P<page>[\d]+)/', views.visits, {}, 'visits'),
    (r'^(?P<user_id>[\w.@+-]+)/new/', views.submit_visit, {}, 'submit-visit'),
    (r'^(?P<user_id>[\w.@+-]+)/visit/(?P<visit_id>[\d]+)/', views.visit, {}, 'visit'),
)
