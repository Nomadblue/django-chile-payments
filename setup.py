#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='django-chile-payments',
    version='0.2.0',
    description='Chilean payment brokers for Django',
    long_description=read_md('README.md'),
    packages=find_packages(),
    url='https://github.com/Nomadblue/django-chile-payments',
    license='MIT',
    author='José Sazo',
    author_email='jose.sazo@gmail.com',
    include_package_data=True,
    install_requires=['pycrypto', 'requests', 'rsa'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
