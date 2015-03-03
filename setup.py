# -*- encoding: utf-8 -*-

from setuptools import setup


setup(
    name='apt-config-tool',
    version='0.0.1',
    description='Set up apt and install packages as part of a scripted provisioning process (such as building a Dockerfile).',
    author='Kevin Kelley',
    author_email='kelleyk@kelleyk.net',
    url='http://github.com/kelleyk/apt-config-tool',
    packages=['apt_config_tool'],
    install_requires=[
        'pyyaml',
        'intensional',
        ],
    entry_points=dict(
        console_scripts=[
            'apt-config-tool = apt_config_tool:main',
        ],
    ),
)
