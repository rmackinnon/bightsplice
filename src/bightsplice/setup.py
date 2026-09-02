from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import bightsplice

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md', 'CHANGES.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='bightsplice',
    version=bightsplice.__version__,
    url='<github_project_url>',
    license='<license>',
    author='<your_name>',
    author_email='your@email.at',
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    description='<desc>',
    long_description=long_description,
    packages=['bightsplice'],
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: <LICENSE>',
        'Operating System :: OS Independent'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)