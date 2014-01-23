from django.template import Template, Context


def test_qurl_append():
    out = Template(
        '{% load qurl %}'
        '{% qurl "http://example.com/?a=1" a+="2" a-="1" %}'
    ).render(Context())
    assert out == 'http://example.com/?a=2'


def test_qurl_set():
    out = Template(
        '{% load qurl %}'
        '{% qurl "http://example.com/?a=1" a=None b="1" %}'
    ).render(Context())
    assert out == 'http://example.com/?b=1'


def test_qurl_as():
    context = Context()
    Template(
        '{% load qurl %}'
        '{% qurl "http://example.com/?a=1" a=None as url %}'
    ).render(context)
    assert context.get('url') == 'http://example.com/'
