from setuptools import setup, find_packages

setup(
    name='pulp_report',
    version='0.1.dev0',
    license='GPLv2+',
    packages=find_packages(exclude=['test', 'test.*']),
    author='Uli Fouquet',
    author_email='uli@gnufix.de',
    entry_points = {
        'pulp.extensions.admin': [
        'report_admin = pulp_report.extensions.admin.pulp_cli:initialize',
        ]
    }
)
