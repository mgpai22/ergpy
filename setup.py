from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ergpy',
    version='0.1.0',
    description='Python-jvm wrapper for interacting with the Ergo Blockchain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mgpai22/ergpy',
    author='MGpai',
    license='MIT',
    keywords='appkit',
    include_package_data=True,
    packages=['ergpy'],
    install_requires=['requests']
)