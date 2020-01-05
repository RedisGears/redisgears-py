from setuptools import setup, find_packages

requirements = list(map(str.strip, open("requirements.txt").readlines()))

setup(
    name='gearsclient',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)