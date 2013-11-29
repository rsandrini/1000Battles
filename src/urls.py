from django.conf.urls import patterns, include, url
from core import urls
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('core.urls')),
)
#urlpatterns += staticfiles_urlpatterns()

