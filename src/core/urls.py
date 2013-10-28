from django.conf.urls import patterns, include, url
from core.views import *


urlpatterns = patterns('',
    #url(r'^/', include('src.core.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^dashboard/(?P<id>\d+)/$', DashboardView.as_view(), name="dashboard"),
)
