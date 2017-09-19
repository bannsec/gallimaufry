# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys
from version import version

here = os.path.abspath(os.path.dirname(__file__))

long_description = "See website for more info."

setup(
    name='usb_pcap',
    version=version,
    description='Tool to ease parsing of USB information out of pcaps',
    long_description=long_description,
    url='https://github.com/owlz/usb_pcap',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    extras_require={
        'dev': ['six','ipython','twine','pytest','python-coveralls','coverage','pytest-cov','pytest-xdist','sphinxcontrib-napoleon', 'sphinx_rtd_theme','sphinx-autodoc-typehints'],
    },
    install_requires=["enforce"],
    keywords='usb pcap parse',
    packages=find_packages(exclude=['contrib', 'docs', 'tests','lib','examples']),
)

