""" Test settings for Django """

INSTALLED_APPS = (
    'qurl',
)

TEMPLATE_DEBUG = True
SECRET_KEY = "super secret key"
ROOT_URLCONF = 'tests.urls'