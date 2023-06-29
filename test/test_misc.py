import unittest
from collections import OrderedDict

from src.misc import items
from src.misc import asFunction
from src.misc import filterByKey
from src.misc import HashCache


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
            self.assertEquals(type(input), cache.get(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEquals(type(input), cache.set(
                cache.key(input), input, type(input)))

        for input in inputs:
            self.assertEquals(input, cache.set(
                cache.key(input), input, type(input)))

        for input in inputs:
            self.assertEquals(input, cache.delete(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEquals(type(input), cache.delete(
                cache.key(input), type(input)))

        for input in inputs:
            self.assertEquals(type(input), cache.get(
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
