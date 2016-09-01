import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pulp_report',
    version='0.1.dev0',
    license='GPLv2+',
    long_description=read('README.rst') + '\n\n\n' + read('CHANGES.rst'),
    packages=find_packages(exclude=['test', 'test.*']),
    author='Uli Fouquet',
    author_email='uli@gnufix.de',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={
        'pulp.extensions.admin': [
            'report_admin = pulp_report.extensions.admin.pulp_cli:initialize',
        ]
    }
)
