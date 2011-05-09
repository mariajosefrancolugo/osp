from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('osp.api.urls')),
    (r'^assessment/', include('osp.assessments.urls', namespace='assessment',
        app_name='assessment')),
    #(r'^note/', include('osp.notes.urls')),
    (r'^profile/', include('osp.profiles.urls', namespace='profile',
        app_name='profile')),
    #(r'^report/', include('osp.reports.urls')),
    #(r'^roster/', include('osp.rosters.urls', namespace='roster',
    #    app_name='roster')),
    #(r'^survey/', include('osp.surveys.urls')),
    (r'^', include('osp.core.urls', namespace='core', app_name='core')),

    (r'^admin/', include(admin.site.urls)),
)

if settings.AUTHENTICATION_BACKEND == 'CAS':
    urlpatterns += patterns('django_cas.views',
        (r'^login/$', 'login', {}, 'login'),
        (r'^logout/$', 'logout', {}, 'logout'),
    )
else:
    urlpatterns += patterns('django.contrib.auth.views',
        (r'^login/$', 'login', {}, 'login'),
        (r'^logout/$', 'logout', {}, 'logout'),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}, 'static'),
    )
