# redisgears-py
[RedisGears](http://redisgears.io) python client

## Example: Using the Python Client:
```python
from gearsclient import GearsRemoteBuilder as GRB
import redis

conn = redis.Redis(host='localhost', port=6379)

# count for each genre how many times it appears

res = GRB('KeysOnlyReader', r=conn).\
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