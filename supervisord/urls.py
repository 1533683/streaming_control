from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'supervisord.views.supervisord'),
    url(r'^api/supervisord/$', 'supervisord.views.supervisord_json'),
    url(r'^api/(?P<name>.+)/$', 'supervisord.views.action'),
)
