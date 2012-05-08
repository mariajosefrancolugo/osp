from django.conf.urls.defaults import *
from django.conf import settings

from osp.assessments import views

urlpatterns = patterns('',
    (r'^personality-type/$', views.personality_type, {}, 'personality-type'),
    (r'^personality-type/results/(?P<result_id>\d+)/$',
        views.personality_type_results, {}, 'personality-type-results'),
    (r'^learning-style/$', views.learning_style, {}, 'learning-style'),
    (r'^learning-style/results/(?P<result_id>\d+)/$',
        views.learning_style_results, {}, 'learning-style-results'),
)

try:
    url_extensions =  settings.EXTEND_ASSESSMENTS_URLS
except:
    url_extensions = []
for assessment_url in url_extensions:
    urlpatterns += patterns('',
        (r'^%s' % assessment_url['path'], include('%s' % assessment_url['file'])),
)
