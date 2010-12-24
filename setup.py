#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-auth-utils',
    version=__import__('auth_utils').__version__,
    description='Helper classes that allow Django to authenticate with an email address as the username',
    author='Paul Watts',
    author_email='paulcwatts@gmail.com',
    url='http://github.com/paulcwatts/django-auth-utils/',
    license='BSD',
    packages=find_packages(),
)
