import six
if six.PY3:
    from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode
else:
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode

from django.utils.encoding import smart_str


def qurl(url, add=None, exclude=None, remove=None):
    """
    Returns the url with changed parameters
    """
    urlp = list(urlparse(url))
    qp = parse_qsl(urlp[4])

    # Add parameters
    add = add if add else {}
    for name, value in add.items():
        if isinstance(value, (list, tuple)):
            # Append mode
            value = [smart_str(v) for v in value]
            qp = [p for p in qp if p[0] != name or p[1] not in value]
            qp.extend([(name, smart_str(val)) for val in value])
        else:
            # Set mode
            qp = [p for p in qp if p[0] != name]
            qp.append((name, smart_str(value)))

    # Exclude parameters
    exclude = exclude if exclude else {}
    for name, value in exclude.items():
        if not isinstance(value, (list, tuple)):
            value = [value]
        value = [smart_str(v) for v in value]
        qp = [p for p in qp if p[0] != name or p[1] not in value]

    # Remove parameters
    remove = remove if remove else []
    for name in remove:
        qp = [p for p in qp if p[0] != name]

    urlp[4] = urlencode(qp, True)
    return urlunparse(urlp)
