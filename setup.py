from os.path import join
from setuptools import setup, find_packages

with open(join('wotw_xcb', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

setup(
    name='wotw-xcb',
    version=__version__,
    packages=find_packages(),
    package_data={
        '': [
            'VERSION',
        ]
    },
    include_package_data=True
)
