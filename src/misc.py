from xxhash import xxh32
import jsonpickle
import ramda as R
from json import dumps, loads


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
            if len(args) < 1:
                return wannabe

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


def createCaster(item: any) -> callable:

    if item is None:
        return lambda x: None

    cls = None
    try:
        cls = item.__class__
    except Exception as e:
        print(e)
        pass
    if not callable(cls):
        def cls(x): return x

    return cls


def clone(item: any) -> any:

    def isMutable(item):
        return item is not None and not callable(item) and not isinstance(item, (str, float, int))

    cls = createCaster(item)

    if not isinstance(item, str):
        try:
            res = R.map(
                lambda item: clone(item) if isMutable(item) else item
            )(item)
            try:
                return cls(res)
            except Exception as e:
                print(e)
            return res
        except TypeError as e:
            pass
        except Exception as e:
            print(e)
            pass

    return cls(loads(dumps(item))) \
        if isMutable(item) else item
