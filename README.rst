Append, remove or replace query string parameters from a url (preserve order).
Originally created by Sophilabs - https://github.com/sophilabs/django-qurl-templatetag



Installation
============
.. code-block::

    pip install -e git+https://github.com/obiwanus/django-qurl.git#egg=django-qurl

Usage in templates
==================

Example:

.. code-block::

    {% load qurl %}

    {% qurl '/search?page=1&color=blue&color=green' order=name page-- color+=red color-=green %}
    Output: /search?color=blue&order=name&color=red

    {% qurl request.get_full_path order='name' %}
    Output: /your/current/path/?order=name

Parameters:

.. code-block::

    name=value: replace all values of name by one value
    name--: remove all values of name
    name+=value: append a new value for name
    name-=value: remove the value of name with the value

Using reverse in the template tag:

.. code-block::

    {% qurl 'url_name' [reverse_params] | order=name color+=red color+=green %}
    Output: /reversed/url/?order=name&color=red&color=green

The reverse syntax is exactly the same as in the standard Django ``{% url %}``
tag.


Usage in views
==============

Examples:

.. code-block:: python

    from qurl import qurl

    url = '/testurl/1/'
    qurl(url, add={'a': 'a1', 'b': ['b1', 'b2']})
    # Output: /testurl/1/?a=a1&b=b1&b=b2

    url = '/testurl/1/?a=a1&b=b1&b=b2'
    qurl(url, add={'a': 'a2'}, remove=['b'])
    # Output: /testurl/1/?a=a2

    url = '/testurl/1/?a=a1&b=b1&b=b2'
    qurl(url, add={'a': ['a2']}, remove=['b'])
    # Output: /testurl/1/?a=a1&a=a2

    url = '/testurl/1/?a=a1&b=b1&b=b2'
    qurl(url, exclude={'b': 'b2'}, add={'a': 'a2'})
    # Output: /testurl/1/?a=a1&a=a2&b=b1

    # You can use request.GET as a base
    url = '/testurl/1/'
    qurl(url, add=request.GET, exclude={'b': 'b1'}

Notes:
------

If you want to assign a specific value to the parameter (replacing all
existing values), use ``add={'param': 'value'}``.

If you want to add a value to already existing ones, use
``add={'param': ['value']}``. You can add more than one value of course.

Please check the tests for more usage examples.


Running tests
-------------

Please make sure `tox <http://tox.testrun.org/>`_ is installed and run
``tox`` from the command line.