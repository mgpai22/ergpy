"""
Dynamic metadata configuration
==============================

setup.py is the build script for setuptools. It tells setuptools
about your package (such as the name and version) as well as which
code files to include.

Ref: https://packaging.python.org/en/latest/tutorials/packaging-projects/

AUTHOR
    mgpai22@GitHub

CREATED AT
    Wed. 20 Apr. 2022 23:43
"""
# External packages import
from setuptools import setup

# README.md as description
with open('./README.md', 'r') as fp:
    long_description: str = fp.read()

# Required packages
packages: str = """
setuptools>=40.8.0
JPype1>=1.3.0
requests>=2.27.1
stubgenj>=0.2.5
"""

# Metadata configuration
setup(
    name='ergpy',
    version='0.1.9.0',
    description='Python-jvm wrapper for interacting with the Ergo Blockchain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mgpai22/ergpy',
    author='MGpai',
    license='MIT',
    keywords='appkit',
    include_package_data=True,
    packages=['ergpy'],
    install_requires=packages.split('\n')
)
