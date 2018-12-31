"""
describes this package for distribution and installation
"""

import os
from setuptools import setup


def _read_file_for_long_description(fname):
    """Read a file and return its content

    :param fname: name of the file to extract the long description from

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# pylint: disable=exec-used
# get version string variable __version__
exec(open('vup/version.py').read())

DESCRIPTION = ("A tool for bumping your version number")

setup(
    name='vup',
    # pylint: disable=undefined-variable
    version=__version__,
    download_url='https://github.com/arecarn/vup/tarball/' + __version__,
    license='MIT',
    description=DESCRIPTION,
    long_description=_read_file_for_long_description('README.md'),
    author='Ryan Carney',
    author_email='arecarn@gmail.com',
    url='https://github.com/arecarn/vup',
    packages=['vup'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={'console_scripts': ['vup=vup.__main__:main']},
)
