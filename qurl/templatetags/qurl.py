import re
import django
from django.template.defaulttags import URLNode

from django.utils.encoding import smart_str
from django.template import Library, Node, TemplateSyntaxError
from django.utils import six
from django.core.urlresolvers import reverse

if six.PY3:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
else:
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode


register = Library()


def _get_url_node(parser, bits):
    """
    Parses the expression as if it was a normal url tag. Was copied
    from the original function django.template.defaulttags.url,
    but unnecessary pieces were removed.
    """
    viewname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    bits = bits[2:]

    if len(bits):
        kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return URLNode(viewname, args, kwargs, asvar=None)


@register.tag
def qurl(parser, token):
    """
    Append, remove or replace query string parameters (preserve order)

        {% qurl url [param]* [as <var_name>] %}

        {% qurl 'reverse_name' [reverse_params] | [param]* [as <var_name>] %}

    param:
            name=value: replace all values of name by one value
            name=None: remove all values of name
            name+=value: append a new value for name
            name-=value: remove the value of name with the value

    Example::

        {% qurl '/search?page=1&color=blue&color=green'
                 order='name' page=None color+='red' color-='green' %}
        Output: /search?color=blue&order=name&color=red

        {% qurl request.get_full_path order='name' %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            '"{0}" takes at least one argument (url)'.format(bits[0]))

    if bits.count('|') > 1:
        raise TemplateSyntaxError(
            '"{0}" may take only one separator'.format(bits[0]))

    if bits.count('|'):
        # A url expression was passed, needs reversing
        url = _get_url_node(parser, bits[:bits.index('|')])
        bits = bits[bits.index('|')+1:]
    else:
        # A url was passed directly
        url = parser.compile_filter(bits[1])
        bits = bits[2:]

    asvar = None
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    qs = []
    if len(bits):
        kwarg_re = re.compile(r"(\w+)(\-=|\+=|=|\-\-)(.*)")
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, op, value = match.groups()
            qs.append((name, op, parser.compile_filter(value),))

    return QURLNode(url, qs, asvar)


class QURLNode(Node):
    """Implements the actions of the qurl tag."""

    def __init__(self, url, qs, asvar):
        self.url = url
        self.qs = qs
        self.asvar = asvar

    def render(self, context):
        if isinstance(self.url, URLNode):
            url = self.url.render(context)
        else:
            url = self.url.resolve(context)
        urlp = list(urlparse(url))
        qp = parse_qsl(urlp[4])
        for name, op, value in self.qs:
            name = smart_str(name)
            value = value.resolve(context)
            value = smart_str(value) if value is not None else None
            if op == '+=':
                qp = [p for p in qp if not(p[0] == name and p[1] == value)]
                qp.append((name, value,))
            elif op == '-=':
                qp = [p for p in qp if not(p[0] == name and p[1] == value)]
            elif op == '=':
                if django.VERSION[0] <= 1 and django.VERSION[1] <= 4:
                    value = value or None
                qp = [p for p in qp if not(p[0] == name)]
                if value is not None:
                    qp.append((name, value,))
            elif op == '--':
                qp = [p for p in qp if not(p[0] == name)]

        urlp[4] = urlencode(qp, True)
        url = urlunparse(urlp)

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url
