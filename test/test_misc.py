import unittest
from collections import OrderedDict
from jsonpickle import encode

from src.misc import items
from src.misc import asFunction
from src.misc import filterByKey
from src.misc import HashCache
from src.misc import createCaster
from src.misc import clone


class testMisc(unittest.TestCase):

    def testItems(self):
        input = 1
        exp = [(None, input)]
        act = [(key, val) for key, val in items(input)]
        self.assertEqual(exp, act)

        input = ['a', 'b', 'c']
        exp = [(key, val) for key, val in enumerate(input)]
        act = [(key, val) for key, val in items(input)]
        self.assertEqual(exp, act)

        input = 'abc'
        exp = [(key, val) for key, val in enumerate(input)]
        act = [(key, val) for key, val in items(input, str_as_vector=True)]
        self.assertEqual(exp, act)
        exp = [(None, input)]
        act = [(key, val) for key, val in items(input, str_as_vector=False)]
        self.assertEqual(exp, act)

        input = ('a', 'b', 'c')
        exp = [(key, val) for key, val in enumerate(input)]
        act = [(key, val) for key, val in items(input)]
        self.assertEqual(exp, act)

        input = set(['a', 'b', 'c'])
        exp = [(key, val) for key, val in enumerate(input)]
        act = [(key, val) for key, val in items(input)]
        self.assertEqual(exp, act)

        input = {
            'A:': 'a',
            'B': 'b',
            'C': 'c',
        }
        exp = [(key, val) for key, val in input.items()]
        act = [(key, val) for key, val in items(input)]
        self.assertEqual(exp, act)

        input = OrderedDict({
            'B': 'b',
            'C': 'c',
            'A:': 'a',
        })
        exp = [(key, input[key]) for key in sorted(input.keys())]
        act = [(key, val) for key, val in items(input, sort=False)]
        self.assertNotEqual(exp, act)
        exp = [(key, input[key]) for key in sorted(input.keys())]
        act = [(key, val) for key, val in items(input, sort=True)]
        self.assertEqual(exp, act)

    def testHashCache(self):

        input = 'a'
        aNum = 1
        aList = [input, aNum]
        aDict = {input: aNum}

        inputs = [input, aNum, aList, aDict]

        cache = HashCache()

        for input in inputs:
            self.assertEqual(type(input), cache.get(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEqual(type(input), cache.set(
                cache.key(input), input, type(input)))

        for input in inputs:
            self.assertEqual(input, cache.set(
                cache.key(input), input, type(input)))

        for input in inputs:
            self.assertEqual(input, cache.delete(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEqual(type(input), cache.delete(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEqual(type(input), cache.get(
                cache.key(input), type(input)))

    def testAsFunction(self):

        specs = [
            {'wannabe': 'abc', 'args': [], 'expected': 'abc'},
            {'wannabe': 'abc', 'args': [1], 'expected': 'abc'},

            {'wannabe': 1, 'args': [], 'expected': 1},
            {'wannabe': 1, 'args': ['a'], 'expected': 1},


            {'wannabe': ['a', 'b'], 'args': [0], 'expected': 'a'},
            {'wannabe': ['a', 'b'], 'args': [1], 'expected': 'b'},

            {'wannabe': {'a': 'A', 'b': 'B'}, 'args': ['a'], 'expected': 'A'},
            {'wannabe': {'a': 'A', 'b': 'B'}, 'args': ['b'], 'expected': 'B'},


            {'wannabe': {'a': ['A0', 'A1'], 'b': ['B0', 'B1']},
                'args': ['a', 0], 'expected': 'A0'},
            {'wannabe': {'a': ['A0', 'A1'], 'b': ['B0', 'B1']},
                'args': ['b', 1], 'expected': 'B1'},

            {'wannabe': [
                {'a': ['0A0', '0A1'], 'b': ['0B0', '0B1']},
                {'a': ['1A0', '1A1'], 'b': ['1B0', '1B1']},
            ], 'args': [0, 'a', 0], 'expected': '0A0'},
            {'wannabe': [
                {'a': ['0A0', '0A1'], 'b': ['0B0', '0B1']},
                {'a': ['1A0', '1A1'], 'b': ['1B0', '1B1']},
            ], 'args': [1, 'a', 1], 'expected': '1A1'},
            {'wannabe': [
                {'a': ['0A0', '0A1'], 'b': ['0B0', '0B1']},
                {'a': ['1A0', '1A1'], 'b': ['1B0', '1B1']},
            ], 'args': [1, 'b', 1], 'expected': '1B1'},

            {'wannabe': 'abcd', 'args': [0],
                'stringAsSingular': False, 'expected': 'a'},
            {'wannabe': 'abcd', 'args': [3],
                'stringAsSingular': False, 'expected': 'd'},
            {'wannabe': ['aBC', 'bCD'], 'args': [0],
                'stringAsSingular': False, 'expected': 'aBC'},
            {'wannabe': ['aBC', 'bCD'], 'args': [1],
                'stringAsSingular': False, 'expected': 'bCD'},
            {'wannabe': ['aBC', 'bCD'], 'args': [0, 2],
                'stringAsSingular': False, 'expected': 'C'},
            {'wannabe': ['aBC', 'bCD'], 'args': [1, 1],
                'stringAsSingular': False, 'expected': 'C'},
        ]

        for spec in specs:
            stringAsSingular = spec['stringAsSingular'] if 'stringAsSingular' in spec else True
            self.assertEqual(spec['expected'], asFunction(spec['wannabe'], stringAsSingular=stringAsSingular)(
                *spec['args']), repr(spec['args']))

    def testFilterByKey(self):

        specs = [
            {'args': [{'a': 1, 'b': 2, 'c': 3}, []], 'expected': {}},
            {'args': [{'a': 1, 'b': 2, 'c': 3}, ['a']], 'expected': {'a': 1}},
            {'args': [{'a': 1, 'b': 2, 'c': 3}, ['c']],
                'expected': {'c': 3}},
            {'args': [{'a': 1, 'b': 2, 'c': 3}, tuple(['a', 'c'])],
                'expected': {'a': 1, 'c': 3}},
            {'args': [{'a': 1, 'b': 2, 'c': 3}, set(['a', 'c'])],
                'expected': {'a': 1, 'c': 3}},
        ]

        for spec in specs:
            self.assertEqual(spec['expected'], filterByKey(
                *spec['args']), repr(spec['args']))

    def testClone(self):

        aNone = None
        aInt = 1
        aStr = 'abc'
        aFloat = 3.333

        def aCallable(x): return x

        aList = [aNone, aInt, aFloat, aStr, aCallable]
        aDict = {
            'a': aNone,
            'b': aInt,
            'c': aFloat,
            'd': aStr,
            'e': aCallable
        }
        aSet = set(aList)
        aTuple = tuple(aList)

        specs = [

            {'args': [aNone], 'kwargs': {}, 'exp': None, 'isImmutable': True},
            {'args': [aInt], 'kwargs': {}, 'exp': aInt, 'isImmutable': True},
            {'args': [aFloat], 'kwargs': {},
                'exp': aFloat, 'isImmutable': True},
            {'args': [aStr], 'kwargs': {}, 'exp': aStr, 'isImmutable': True},
            {'args': [aCallable], 'kwargs': {},
                'exp': aCallable, 'isImmutable': True},

            {'args': [aList], 'kwargs': {}, 'exp': aList},
            {'args': [aDict], 'kwargs': {}, 'exp': aDict},
            {'args': [aSet], 'kwargs': {}, 'exp': aSet},
            {'args': [aTuple], 'kwargs': {}, 'exp': aTuple},

            {
                'args': [[aList, aDict, aSet, aCallable]],
                'kwargs': {},
                'exp': [aList, aDict, aSet, aCallable]
            },
            {
                'args': [tuple([aList, aDict, aSet, aCallable])],
                'kwargs': {},
                'exp': tuple([aList, aDict, aSet, aCallable])
            },
            {
                'args': [{'a': aList, 'b': aDict, 'c': aSet, 'd': aCallable}],
                'kwargs': {},
                'exp': {'a': aList, 'b': aDict, 'c': aSet, 'd': aCallable}
            },
        ]

        for spec in specs:
            act = clone(*spec['args'], **spec['kwargs'])
            exp = spec['exp']
            self.assertEqual(exp, act, encode(spec))
            if 'isImmutable' in spec and spec['isImmutable']:
                self.assertIs(exp, act, encode(spec))
            else:
                self.assertIsNot(exp, act, encode(spec))

    def test_createCaster(self):

        specs = [

            {'typee': None, 'castee': None,
                'expValue': None, 'expType': type(None)},
            {'typee': 3, 'castee': "4",
                'expValue': 4, 'expType': int},
            {'typee': 3.4, 'castee': "5.4",
                'expValue': 5.4, 'expType': float},
            {'typee': "5", 'castee': 6,
                'expValue': "6", 'expType': str},
            {'typee': (5,), 'castee': [6,],
                'expValue': (6,), 'expType': tuple},
            {'typee': set([5, 6]), 'castee': tuple((6, 7)),
                'expValue': set([6, 7]), 'expType': set},
            {'typee': ['ab', lambda x: x], 'castee': (6, 7.0),
                'expValue': [6, 7.0], 'expType': list},
        ]

        for spec in specs:
            caster = createCaster(spec['typee'])
            act = caster(spec['castee'])
            self.assertEqual(spec['expValue'], act, encode(spec))
            self.assertEqual(spec['expType'], type(act), encode(spec))
