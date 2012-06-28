from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('Photo.views',
    url(r'^$', 'index'),
    url(r'^players', 'players'),
    url(r'^board','board'),
    url(r'^move','move'),
    url(r'^poll$','poll'),
)
