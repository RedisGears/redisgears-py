from gearsclient import GearsRemoteBuilder as GRB
from gearsclient import log, hashtag, execute, atomic

counter = 0

def getGB(env, reader='KeysReader'):
    return GRB(reader, r=env.getConnection(), addClientToRequirements=False) 

def test_map(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '2')
    env.cmd('set', 'z', '3')
    res = getGB(env).map(lambda x: x['value']).sort().run()
    env.assertEqual(res, (['1', '2', '3'], []))

def test_filter(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '2')
    env.cmd('set', 'z', '3')
    res = getGB(env).map(lambda x: x['value']).filter(lambda x: x=='1').run()
    env.assertEqual(res, (['1'], []))

def test_foreach(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '2')
    env.cmd('set', 'z', '3')
    def increase(x):
        global counter
        counter += 1

    # important to notice, the counte will increased on the server size and not on client side!!
    res = getGB(env).foreach(increase).map(lambda x: counter).run()
    env.assertEqual(res, ([1, 2, 3], []))

def test_flatmap(env):
    env.cmd('lpush', 'l', '1', '2', '3')
    res = getGB(env, 'KeysOnlyReader').map(lambda x: execute('lrange', x, '0', '-1')).flatmap(lambda x: x).run()
    env.assertEqual(res, (['1', '2', '3'], []))

def test_countby(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).countby().map(lambda x: (x['key'], x['value'])).sort().run()
    env.assertEqual(res, ([('1', 2), ('2', 2)], []))

def test_avg(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).avg().run()
    env.assertEqual(res, ([1.5], []))

def test_count(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).count().run()
    env.assertEqual(res, ([4], []))

def test_distinct(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).distinct().count().run()
    env.assertEqual(res, ([2], []))

def test_aggregate(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).aggregate(0, lambda a, r: a + int(r), lambda a, r: a + r).run()
    env.assertEqual(res, ([6], [])) 

def test_aggregateby(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).aggregateby(lambda x: x, 0, lambda k, a, r: a + int(r), lambda k, a, r: a + r).map(lambda x: (x['key'], x['value'])).sort().run()
    env.assertEqual(res, ([('1', 2), ('2', 4)], []))    

def test_limit(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['value']).sort().limit(1).run()
    env.assertEqual(res, (['1'], []))

def test_sort(env):
    env.cmd('set', 'x', '1')
    env.cmd('set', 'y', '1')
    env.cmd('set', 'z', '2')
    env.cmd('set', 't', '2')
    res = getGB(env).map(lambda x: x['key']).sort().run()
    env.assertEqual(res, (['t', 'x', 'y', 'z'], []))    

def test_hashtag(env):
    res = getGB(env, 'ShardsIDReader').map(lambda x: hashtag()).run()
    env.assertEqual(res, (['06S'], []))

def test_register(env):
    res = getGB(env, 'CommandReader').register(trigger='test')
    env.assertEqual(res, b'OK')
    env.expect('RG.TRIGGER', 'test', 'this', 'is', 'a', 'test').equal([b"['test', 'this', 'is', 'a', 'test']"])   
