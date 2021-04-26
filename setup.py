from setuptools import setup, find_packages
import io

def read_version(version_file):
    """
    Given the input version_file, this function extracts the
    version info from the __version__ attribute.
    """
    version_str = None
    import re
    verstrline = open(version_file, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        version_str = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (version_file,))
    return version_str


def read_all(f):
    with io.open(f, encoding="utf-8") as I:
        return I.read()

requirements = list(map(str.strip, open("requirements.txt").readlines()))

setup(
    name='gearsclient',
    version=read_version("gearsclient/_version.py"),
    description='RedisGears Python Client',
    long_description=read_all("README.md"),
    long_description_content_type='text/markdown',
    url='https://github.com/RedisGears/redisgears-p',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database'
    ],    
    keywords='Redis Gears Extension',
    author='RedisLabs',
    author_email='oss@redislabs.com'
)
