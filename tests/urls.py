from django.conf.urls import patterns, url


def testview(request, *args, **kwargs):
    return None


urlpatterns = patterns('',
    url(r'^testurl/([^/]+)/$', testview, name='testurl'),
    url(r'^testurl-kw/(?P<param>[^/]+)/$', testview, name='testurl_kwargs'),
)