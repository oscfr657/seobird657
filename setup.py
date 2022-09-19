#!/usr/bin/env python

from os import path

from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="SEOBird657",
    version='0.1.1a0',
    description='A small Wagtail app.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Oscar F',
    url='https://github.com/oscfr657/SEOBird657',
    packages=['seobird657'],
    package_dir={'seobird657': '.'},
    package_data={
        'seobird657': [
            './migrations/*',
            './static/*/*/*',
            './static/*/*/*/*',
            './templates/*',
            './templates/*/*',
        ]
    },
    include_package_data=True,
    install_requires=[
        'django',
        'wagtail',
        'wagtailmedia',
    ],
    license='Hippocratic License Version Number: 2.1 with Commons Clause License Condition v1.0',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
