#! /usr/bin/env python2


from setuptools import setup


setup(
    name='aasniff',
    version='0.1.3',
    author='The active archives contributors',
    author_email='alexandre@stdin.fr',
    description='Analyze web ressources and RDF-index them using mime-typed dedicated agents',
    url='http://activearchives.org/',
    packages=['aasniff', 'aasniff.sniffers'],
    include_package_data=True,
    install_requires=[
        'rdflib>=4',
        'html5lib',
        'requests>=1',
        'python-magic',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ]
)
