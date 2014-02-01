django-qurl
-----------

Append, remove or replace query string parameters from an url (preserve order).
Originally created by Sophilabs - https://github.com/sophilabs/django-qurl-templatetag



Installation
============
.. code-block::

    pip install -e git+https://github.com/obiwanus/django-qurl.git#egg=django-qurl

Usage
=====

Append, remove or replace query string parameters from an url (preserve order)

.. code-block::

    {% load qurl %}

    {% qurl url [param]* [as <var_name>] %}

    Parameters:
            name=value: replace all values of name by one value
            name--: remove all values of name
            name+=value: append a new value for name
            name-=value: remove the value of name with the value

    Example:

        {% qurl '/search?page=1&color=blue&color=green' order='name' page=None color+='red' color-='green' %}
        Output: /search?color=blue&order=name&color=red

        {% qurl request.get_full_path order='name' %}
