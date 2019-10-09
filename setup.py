import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
    long_description = fp.read()

setup(
    name='datauri',
    description="implementation of the data uri scheme defined in rfc2397",
    long_description=long_description,
    version='1.0.1',
    author="EclecticIQ",
    author_email="info@eclecticiq.com",
    packages=['datauri'],
    url='https://github.com/eclecticiq/python-data-uri',
    license="BSD",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
