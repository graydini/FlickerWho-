from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Photo.views',
    url(r'^$', 'index'),
    url(r'^players', 'players'),
    url(r'^board','board'),
    url(r'^guess','guess'),
    url(r'^poll$','poll'),
	url(r'^respond$','respond'),
)
