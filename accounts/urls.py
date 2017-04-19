from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # auth
    url(r'^login/$', 'accounts.views.log_in'),
    url(r'^logout', 'accounts.views.log_out'),
    url(r'^password/$', 'accounts.views.password_change'),
    url(r'^profile/$', 'accounts.views.profile'),
    url(r'^api/profile/$', 'accounts.views.profile_json'),
)
