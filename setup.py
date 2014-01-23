from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version = '0.1.0'

setup(
    name='django-qurl',
    version=version,
    author='Ivan Ivanov',
    author_email='ivan@ivanovs.info',
    packages=['qurl'],

    license='MIT',
    url='https://github.com/obiwanus/django-qurl/',

    description="A set of tools to append, remove or replace query string "
                "parameters from a url (originally created by Sophilabs)",
    long_description=open("README.rst").read(),

    requires=['django (>=1.2)'],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
