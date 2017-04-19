from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

urlpatterns = patterns('',
    url(r'^$', 'supervisord.views.supervisord'),
)
