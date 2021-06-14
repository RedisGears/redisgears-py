[![license](https://img.shields.io/github/license/RedisGears/redisgears-py.svg)](https://github.com/RedisGears/redisgears-py)
[![PyPI version](https://badge.fury.io/py/redisgears-py.svg)](https://badge.fury.io/py/redisgears-py)
[![CircleCI](https://circleci.com/gh/RedisGears/redisgears-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGears/redisgears-py/tree/master)
[![GitHub issues](https://img.shields.io/github/release/RedisGears/redisgears-py.svg)](https://github.com/RedisGears/redisgears-py/releases/latest)
[![Codecov](https://codecov.io/gh/RedisGears/redisgears-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisGears/redisgears-py)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/RedisGears/redisgears-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisGears/redisgears-py/context:python)
[![Known Vulnerabilities](https://snyk.io/test/github/RedisJSON/redisjson-py/badge.svg?targetFile=pyproject.toml)](https://snyk.io/test/github/RedisJSON/redisjson-py?targetFile=pyproject.toml)

# redisgears-py
[![Forum](https://img.shields.io/badge/Forum-RedisGears-blue)](https://forum.redislabs.com/c/modules/redisgears)
[![Discord](https://img.shields.io/discord/697882427875393627?style=flat-square)](https://discord.gg/6yaVTtp)

[RedisGears](http://redisgears.io) python client (support python3 only!)

## Example: Using the Python Client:
```python
from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
import redis

conn = redis.Redis(host='localhost', port=6379)

# count for each genre how many times it appears

res = GearsBuilder('KeysOnlyReader', r=conn).\
	  map(lambda x:execute('hget', x, 'genres')).\
	  filter(lambda x:x != '\\N').\
	  flatmap(lambda x: x.split(',')).\
	  map(lambda x: x.strip()).\
	  countby().\
	  run()


for r in res[0]:
	print('%-15s: %d' % (r['key'], r['value']))
```

## Installing
```
pip install git+https://github.com/RedisGears/redisgears-py.git
```
Notice that the library also need to be installed in RedisGears virtual env.

## Developing

1. Create a virtualenv to manage your python dependencies, and ensure it's active.
   ```virtualenv -v venv```
2. Install [pypoetry](https://python-poetry.org/) to manage your dependencies.
   ```pip install poetry```
3. Install dependencies.
   ```poetry install```

[tox](https://tox.readthedocs.io/en/latest/) runs all tests as its default target. Running *tox* by itself will run unit tests. Ensure you have a running redis, with the module loaded.


