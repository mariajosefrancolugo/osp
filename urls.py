from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #(r'^api/', include('osp.api.urls')),
    #(r'^survey/', include('osp.surveys.urls')),
    #(r'^assessment/', include('osp.assessments.urls')),
    #(r'^note/', include('osp.notes.urls')),
    #(r'^report/', include('osp.reports.urls')),
    (r'^', include('osp.core.urls')),

    (r'^admin/', include(admin.site.urls)),
)
