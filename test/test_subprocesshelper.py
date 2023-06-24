import unittest
from collections import OrderedDict
from shlex import split
from os import linesep

from subprocess import run
from src.subprocesshelper import SubProcessHelper


class testSubProcessHelper(unittest.TestCase):

    @classmethod
    def createOutErrSink(cls):

        pairs = {'stdout': {}, 'stderr': {}}
        key = 0

        def outErrSink(out, err):
            nonlocal key
            if out is not None:
                pairs['stdout'][key] = SubProcessHelper.decode(out)

            if err is not None:
                pairs['stderr'][key] = SubProcessHelper.decode(err)

            key += 1

        return outErrSink, pairs

    def testSingleLine(self):
        sink, pairs = self.createOutErrSink()

        self.assertEquals(0, SubProcessHelper.run(
            ["echo", "test run"], outErrSink=sink))

        self.assertEqual([
            'test run\n'
        ], list(pairs['stdout'].values()))
        self.assertEqual([
        ], list(pairs['stderr'].values()))

    def testManyLines(self):
        sink, pairs = self.createOutErrSink()

        self.assertEquals(0, SubProcessHelper.run(
            ['time', '-p', 'echo', 'test run'], outErrSink=sink, shell=True))

        self.assertEqual([
            'test run' + linesep,
        ], list(pairs['stdout'].values()))

        self.assertEqual([
            'real 0.00' + linesep,
            'user 0.00' + linesep,
            'sys 0.00' + linesep,
        ], list(pairs['stderr'].values()))
