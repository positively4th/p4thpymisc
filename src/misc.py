from xxhash import xxh32
import jsonpickle


def items(o, sort=False, str_as_vector=False):
    if str_as_vector or not isinstance(o, str):
        try:
            return sorted(o.items()) if sort else o.items()
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        try:
            return enumerate(sorted(o) if sort else o)
        except TypeError as e:
            pass
        try:
            return enumerate(o)
        except TypeError as e:
            pass

    return {None: o}.items()


def asFunction(wannabe, stringAsSingular=True) -> callable:

    if callable(wannabe):
        return lambda *args, **kwargs: wannabe(*args, **kwargs)

    isIterable = hasattr(wannabe, "__len__") or hasattr(wannabe, "__getitem__")
    isIterable = isIterable and (
        not isinstance(wannabe, str) or not stringAsSingular)

    if isIterable:

        def indexedAsFunction(*args, wbCopy=wannabe):
            val = wbCopy[args[0]]
            return asFunction(val, stringAsSingular=stringAsSingular)(*args[1:]) if len(args) > 1 else val

        return indexedAsFunction

    return lambda *args, **kwargs: wannabe


def filterByKey(d: dict, keepKeys: list | tuple | set) -> dict:
    keys = tuple(set(d.keys()).intersection(set(keepKeys)))
    res = {}
    for key in keys:
        res[key] = d[key]
    return res


class HashCache:

    def __init__(self, hasher=None, serializer=None):
        self.hasher = lambda x: xxh32(
            x).hexdigest() if hasher is None else hasher
        self.serializer = lambda x: jsonpickle.encode(
            x, unpicklable=True) if serializer is None else serializer
        # self.serializer = lambda x: orjson.dumps(x) if serializer is None else serializer
        self.cache = {}

    def key(self, data):
        key = self.hasher(self.serializer([id(data), data]))
        return key

    def get(self, key, res=None):
        return self.cache[key] if key in self.cache else res

    def set(self, key, data, res=None):
        _res = self.get(key) if key in self.cache else res
        self.cache[key] = data
        return _res

    def delete(self, key, res=None):
        if key in self.cache:
            _res = self.cache[key]
            del self.cache[key]
        else:
            _res = res
        return _res
