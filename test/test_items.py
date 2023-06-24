import unittest
from collections import OrderedDict

from src.misc import items


class testStandardTypes(unittest.TestCase):

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
