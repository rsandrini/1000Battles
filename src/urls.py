from django.conf.urls import patterns, include, url
from core import urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
