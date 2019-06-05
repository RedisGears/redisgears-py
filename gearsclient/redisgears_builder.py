import redis
import cloudpickle
import pickle

class GearsRemoteMapStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.map(self.callback)

class GearsRemoteForeachStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.foreach(self.callback)

class GearsRemoteFlatMapStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.flatmap(self.callback)

class GearsRemoteFilterStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.filter(self.callback)

class GearsRemoteCountByStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.countby(self.callback)

class GearsRemoteAvgByStep():
    def __init__(self, callback):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        self.callback.__globals__.update(globalsDict)
        gb.avg(self.callback)

class GearsRemoteCountStep():
    def __init__(self):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        gb.count()

class GearsRemoteDistinctStep():
    def __init__(self):
        self.callback = callback

    def AddToGB(self, gb, globalsDict):
        gb.distinct()

class GearsRemoteAggregateStep():
    def __init__(self, zero, seqOp, combOp):
        self.zero = zero
        self.seqOp = seqOp
        self.combOp = combOp

    def AddToGB(self, gb, globalsDict):
        self.seqOp.__globals__.update(globalsDict)
        self.combOp.__globals__.update(globalsDict)
        gb.aggregate(self.zero, self.seqOp, self.combOp)

class GearsRemoteAggregateByStep():
    def __init__(self, extractor, zero, seqOp, combOp):
        self.extractor = extractor
        self.zero = zero
        self.seqOp = seqOp
        self.combOp = combOp

    def AddToGB(self, gb, globalsDict):
        self.seqOp.__globals__.update(globalsDict)
        self.combOp.__globals__.update(globalsDict)
        gb.aggregate(self.extractor, self.zero, self.seqOp, self.combOp)

class GearsRemoteSortStep():
    def __init__(self, reverse):
        self.reverse = reverse

    def AddToGB(self, gb, globalsDict):
        gb.sort(self.reverse)

class GearsRemoteLimitStep():
    def __init__(self, count, offset):
        self.count = count
        self.offset = offset

    def AddToGB(self, gb, globalsDict):
        gb.limit(self.count, self.offset)

class GearsRemoteRunStep():
    def __init__(self, arg, convertToStr, collect):
        self.arg = arg
        self.convertToStr = convertToStr
        self.collect = collect

    def AddToGB(self, gb, globalsDict):
        gb.run(self.arg, self.convertToStr, self.collect)

class GearsRemoteRegisterStep():
    def __init__(self, arg):
        self.arg = arg

    def AddToGB(self, gb, globalsDict):
        gb.register(self.arg) if self.arg else gb.register()


class GearsPipe():
    def __init__(self, reader='KeysReader', defaultArg='*'):
        self.reader = reader
        self.defaultArg = defaultArg
        self.steps = []

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

    def run(self, arg, convertToStr, collect):
        self.steps.append(GearsRemoteRunStep(arg, convertToStr, collect))

    def register(self, arg):
        self.steps.append(GearsRemoteRegisterStep(arg))


class GearsRemoteBuilder():
    def __init__(self, reader='KeysReader', defaultArg='*', r=None):
        if r is None:
            r = redis.Redis()
        self.r = r
        self.pipe = GearsPipe(reader, defaultArg)

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
        self.pipe.countby(callback)
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

    def run(self, arg=None, convertToStr=False, collect=True):
        self.pipe.run(arg, convertToStr, collect)
        selfBytes = cloudpickle.dumps(self.pipe)
        results = self.r.execute_command('RG.PYEXECUTEREMOTE', selfBytes)
        res, errs = results
        res = [cloudpickle.loads(record) for record in res]
        return res, errs

    def register(self, arg=None):
        self.pipe.register(arg)
        selfBytes = cloudpickle.dumps(self.pipe)
        res = self.r.execute_command('RG.PYEXECUTEREMOTE', selfBytes)
        return res
