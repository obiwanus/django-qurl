import os
from django.template import Template, Context


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'


def test_append():
    out = Template(
        "{% load qurl %}"
        "{% qurl 'http://example.com/?a=1&b=3' a+=2 a-=1 %}"
    ).render(Context())
    assert 'b=3' in out
    assert 'a=2' in out


def test_set():
    out = Template(
        "{% load qurl %}"
        "{% qurl 'http://example.com/?a=1&b=2' b=1 %}"
    ).render(Context())
    assert 'b=2' not in out
    assert 'b=1' in out
    assert 'a=1' in out


def test_qurl_as():
    context = Context()
    template = Template(
        "{% load qurl %}"
        "{% qurl 'http://example.com/?a=1' a-- as url1 %}"
        "-{{ url1 }}-"
    )
    assert template.render(context) == '-http://example.com/-'
