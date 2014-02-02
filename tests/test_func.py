from __future__ import unicode_literals

from qurl import qurl


def test_add():
    url = '/testurl/12/'
    out = qurl(url, add={'a': 'a1', 'b': ['b1', 'b2']})
    assert 'a=a1' in out
    assert 'b=b1' in out
    assert 'b=b2' in out


def test_set():
    url = '/testurl/1/?a=1&b=12'
    out = qurl(url, add={'a': 2, 'b': ['b1']})
    assert 'a=2' in out
    assert 'a=1' not in out
    assert 'b=12' in out
    assert 'b=b1' in out


def test_exclude():
    url = '/testurl/13/?p=2&p=vasia&p=3'
    out = qurl(url, exclude={'p': ['2', 3]})
    assert 'p=2' not in out
    assert 'p=3' not in out
    assert 'p=vasia' in out


def test_remove():
    url = '/testurl/13/?a=2&a=vasia&b=3&c=5'
    out = qurl(url, remove=['a', 'b'])
    assert 'a=' not in out
    assert 'b=' not in out
    assert 'c=5' in out


def test_blank_str():
    url = '/testurl/13/?a=2&a=vasia'
    out = qurl(url, add={'a': '', 'b': None})
    assert out == '/testurl/13/?a=&b=None'
