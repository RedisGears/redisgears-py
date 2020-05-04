from gearsclient import GearsRemoteBuilder as GRB
from gearsclient import log, hashtag, execute, atomic
import redis

conn = redis.Redis(host='localhost', port=6379)

# count for each genre how many times it appears

# class test:
#     def __init__(self):
#         self.count = 1

# def func1(x):
#     return test()

# def func2(x):
#     x.count += 1
#     return x

def func(x):
    with atomic():
        execute('hset', 'h', 'foo', 'bar')
        execute('hset', 'h', 'foo1', 'bar1')
    return x

res = GRB('ShardsIDReader',r=conn).\
      map(func).\
      run()

print(res)
# if len(res[1]) > 0:
#     print(res[1])

# for r in res[0]:
#     print('%s' % str(r.count))
