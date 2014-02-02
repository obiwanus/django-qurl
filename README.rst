django-qurl
-----------

Append, remove or replace query string parameters from a url (preserve order).
Originally created by Sophilabs - https://github.com/sophilabs/django-qurl-templatetag



Installation
============
.. code-block::

    pip install -e git+https://github.com/obiwanus/django-qurl.git#egg=django-qurl

Usage
=====

Parameters:

.. code-block::

    name=value: replace all values of name by one value
    name--: remove all values of name
    name+=value: append a new value for name
    name-=value: remove the value of name with the value

Example:

.. code-block::

    {% load qurl %}

    {% qurl '/search?page=1&color=blue&color=green' order=name page-- color+=red color-=green %}
    Output: /search?color=blue&order=name&color=red

    {% qurl request.get_full_path order='name' %}
    Output: /your/current/path/?order=name

Using reverse in the template tag:

.. code-block::

    {% qurl 'url_name' [reverse_params] | order=name color+=red color+=green %}
    Output: /reversed/url/?order=name&color=red&color=green

The reverse syntax is exactly the same as in the standard Django ``{% url %}``
tag.
