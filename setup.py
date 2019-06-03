from setuptools import setup, find_packages
setup(
    name='gearsclient',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'redis',
        'cloudpickle'
    ],
)