from django.conf.urls.defaults import *

from osp.interventions import views

urlpatterns = patterns('',
    (r'^compose/', views.compose_intervention, {}, 'compose-intervention'),
    (r'^submit/', views.submit_intervention, {}, 'submit-intervention'),
)
