#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    "rpyc",
    "slash",
    "uiautomator",
    "bunch",
    "selenium",
    "Skype4py",
    "baker",
    "SQLAlchemy",
    "IMAPClient",
]

test_requirements = [
    "slash",
]

setup(
    name='sr_automation',
    version='0.1.0',
    description='SunRiver testing automation framework',
    long_description=readme + '\n\n' + history,
    #author='Barak Bercovitz',
    #author_email='barak@wizery.com',
    #url='https://github.com/barakber/sr_automation',
    packages= find_packages(),
    package_dir={
        'sr_automation': 'sr_automation',
        'sr_tests': 'sr_tests',
        'sr_tools': 'sr_tools',
        },
    include_package_data=True,
    install_requires=requirements,
    #license="BSD",
    zip_safe=False,
    keywords='sr_automation',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points = {
        'console_scripts': [
            'sr_tool = sr_tools.sr_tool:main',
            ],
        }
)
