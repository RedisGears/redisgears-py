import redis
import cloudpickle
import pickle

class GearsRemoteLocalGroupByStep():
    def __init__(self, extractor, reducer):
        self.extractor = extractor
        self.reducer = reducer

    def AddToGB(self, gb):
        gb.localgroupby(self.extractor, self.reducer)

class GearsRemoteAccumulateStep():
    def __init__(self, accumulator):
        self.accumulator = accumulator

    def AddToGB(self, gb):
        gb.accumulate(self.accumulator)

class GearsRemoteRepartitionStep():
    def __init__(self, extractor):
        self.extractor = extractor

    def AddToGB(self, gb):
        gb.repartition(self.extractor)

class GearsRemoteMapStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.map(self.callback)

class GearsRemoteForeachStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.foreach(self.callback)

class GearsRemoteFlatMapStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.flatmap(self.callback)

class GearsRemoteFilterStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.filter(self.callback)

class GearsRemoteCountByStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.countby(self.callback)

class GearsRemoteAvgStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb):
        gb.avg(self.callback)

class GearsRemoteCountStep():
    def __init__(self):
        pass

    def AddToGB(self, gb):
        gb.count()

class GearsRemoteDistinctStep():
    def __init__(self):
        pass

    def AddToGB(self, gb):
        gb.distinct()

class GearsRemoteAggregateStep():
    def __init__(self, zero, seqOp, combOp):
        self.zero = zero
        self.seqOp = seqOp
        self.combOp = combOp

    def AddToGB(self, gb):
        gb.aggregate(self.zero, self.seqOp, self.combOp)

class GearsRemoteAggregateByStep():
    def __init__(self, extractor, zero, seqOp, combOp):
        self.extractor = extractor
        self.zero = zero
        self.seqOp = seqOp
        self.combOp = combOp

    def AddToGB(self, gb):
        gb.aggregateby(self.extractor, self.zero, self.seqOp, self.combOp)

class GearsRemoteSortStep():
    def __init__(self, reverse):
        self.reverse = reverse

    def AddToGB(self, gb):
        gb.sort(self.reverse)

class GearsRemoteLimitStep():
    def __init__(self, count, offset):
        self.count = count
        self.offset = offset

    def AddToGB(self, gb):
        gb.limit(self.count, self.offset)

class GearsRemoteRunStep():
    def __init__(self, arg, convertToStr, collect, kargs):
        self.arg = arg
        self.convertToStr = convertToStr
        self.collect = collect
        self.kargs = kargs

    def AddToGB(self, gb):
        gb.run(self.arg, self.convertToStr, self.collect, **self.kargs)

class GearsRemoteRegisterStep():
    def __init__(self, prefix, convertToStr, collect, kargs):
        self.prefix = prefix
        self.convertToStr = convertToStr
        self.collect = collect
        self.kargs = kargs

    def AddToGB(self, gb):
        gb.register(self.prefix, self.convertToStr, self.collect, **self.kargs)


class GearsPipe():
    def __init__(self, reader='KeysReader', defaultArg='*'):
        self.reader = reader
        self.defaultArg = defaultArg
        self.steps = []

    def localgroupby(self, extractor, reducer):
        self.steps.append(GearsRemoteLocalGroupByStep(extractor, reducer))
        return self

    def accumulate(self, accumulator):
        self.steps.append(GearsRemoteAccumulateStep(accumulator))
        return self

    def repartition(self, extractor):
        self.steps.append(GearsRemoteRepartitionStep(extractor))
        return self

    def map(self, callback):
        self.steps.append(GearsRemoteMapStep(callback))
        return self

    def foreach(self, callback):
        self.steps.append(GearsRemoteForeachStep(callback))
        return self

    def flatmap(self, callback):
        self.steps.append(GearsRemoteFlatMapStep(callback))
        return self

    def filter(self, callback):
        self.steps.append(GearsRemoteFilterStep(callback))
        return self

    def countby(self, callback):
        self.steps.append(GearsRemoteCountByStep(callback))
        return self

    def avg(self, callback):
        self.steps.append(GearsRemoteAvgStep(callback))
        return self

    def count(self):
        self.steps.append(GearsRemoteCountStep())
        return self

    def distinct(self):
        self.steps.append(GearsRemoteDistinctStep())
        return self

    def aggregate(self, zero, seqOp, combOp):
        self.steps.append(GearsRemoteAggregateStep(zero, seqOp, combOp))
        return self

    def aggregateby(self, extractor, zero, seqOp, combOp):
        self.steps.append(GearsRemoteAggregateByStep(extractor, zero, seqOp, combOp))
        return self

    def sort(self, reverse):
        self.steps.append(GearsRemoteSortStep(reverse))
        return self

    def limit(self, count, offset):
        self.steps.append(GearsRemoteLimitStep(count, offset))
        return self

    def run(self, arg, convertToStr, collect, **kargs):
        self.steps.append(GearsRemoteRunStep(arg, convertToStr, collect, kargs))

    def register(self, prefix, convertToStr, collect, **kargs):
        self.steps.append(GearsRemoteRegisterStep(prefix, convertToStr, collect, kargs))

    def createAndRun(self, GB):
        gb = GB(self.reader)
        for s in self.steps:
            s.AddToGB(gb)



class GearsRemoteBuilder():
    def __init__(self, reader='KeysReader', defaultArg='*', r=None, requirements=[], addClientToRequirements=True):
        if r is None:
            r = redis.Redis()
        self.r = r
        self.pipe = GearsPipe(reader, defaultArg)
        self.requirements = requirements
        if addClientToRequirements:
            self.requirements += ['gearsclient==1.0.1']
        if len(self.requirements) > 0:
            self.requirements = ['REQUIREMENTS'] + self.requirements

    def localgroupby(self, extractor, reducer):
        self.pipe.localgroupby(extractor, reducer)
        return self

    def accumulate(self, accumulator):
        self.pipe.accumulate(accumulator)
        return self

    def repartition(self, extractor):
        self.pipe.repartition(extractor)
        return self

    def map(self, callback):
        self.pipe.map(callback)
        return self

    def foreach(self, callback):
        self.pipe.foreach(callback)
        return self

    def flatmap(self, callback):
        self.pipe.flatmap(callback)
        return self

    def filter(self, callback):
        self.pipe.filter(callback)
        return self

    def countby(self, callback=lambda x: x):
        self.pipe.countby(callback)
        return self

    def avg(self, callback=lambda x: float(x)):
        self.pipe.avg(callback)
        return self

    def count(self):
        self.pipe.count()
        return self

    def distinct(self):
        self.pipe.distinct()
        return self

    def aggregate(self, zero, seqOp, combOp):
        self.pipe.aggregate(zero, seqOp, combOp)
        return self

    def aggregateby(self, extractor, zero, seqOp, combOp):
        self.pipe.aggregateby(extractor, zero, seqOp, combOp)
        return self

    def sort(self, reverse=True):
        self.pipe.sort(reverse)
        return self

    def limit(self, count, offset=0):
        self.pipe.limit(count, offset)
        return self

    def run(self, arg=None, collect=True, **kargs):
        self.map(lambda x: cloudpickle.dumps(x))
        self.pipe.run(arg, False, collect)
        selfBytes = cloudpickle.dumps(self.pipe)
        serverCode = '''
import cloudpickle
p = cloudpickle.loads(%s)
p.createAndRun(GB)
        ''' % selfBytes
        results = self.r.execute_command('RG.PYEXECUTE', serverCode, *self.requirements)
        res, errs = results
        res = [cloudpickle.loads(record) for record in res]
        return res, errs

    def register(self, prefix='*', convertToStr=True, collect=True, **kargs):
        self.pipe.register(prefix, convertToStr, collect, **kargs)
        selfBytes = cloudpickle.dumps(self.pipe)
        serverCode = '''
import cloudpickle
p = cloudpickle.loads(%s)
p.createAndRun(GB)
        ''' % selfBytes
        res = self.r.execute_command('RG.PYEXECUTE', serverCode, *self.requirements)
        return res

def log(msg, level='notice'):
    from redisgears import log as redisLog
    redisLog(msg, level=level)

def gearsConfigGet(key, default=None):
    from redisgears import config_get as redisConfigGet
    val = redisConfigGet(key)
    return val if val is not None else default

def execute(*args):
    from redisgears import executeCommand as redisExecute
    return redisExecute(*args)

def hashtag():
    from redisgears import getMyHashTag as redisHashtag
    return redisHashtag()

class atomic:
    def __init__(self):
        from redisgears import atomicCtx as redisAtomic
        self.atomic = redisAtomic()
        pass

    def __enter__(self):
        self.atomic.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.atomic.__exit__()


