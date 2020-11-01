from gearsclient import GearsRemoteBuilder as GRB
from gearsclient import execute, atomic
import redis

conn = redis.Redis(host='localhost', port=6379)

def func(x):
    with atomic():
        execute('hset', 'h', 'foo', 'bar')
        execute('hset', 'h', 'foo1', 'bar1')
    return x

res = GRB('ShardsIDReader',r=conn).\
      map(func).\
      run()

print(res)
