# pylint: disable=missing-docstring,unused-argument,invalid-name
# pylint: disable=no-self-use,protected-access
from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from xcb.xproto import Atom

from wotw_x11_comparison.common import MovesMouse, RunsComparisons, WritesResults


class RunsComparisonsTestCase(TestCase):

    def setUp(self):
        writes_results_patcher = patch.object(
            WritesResults,
            '__init__',
            # 'wotw_x11_comparison.common.writes_results.__init__',
            return_value=MagicMock()
        )
        self.mock_writes_results = writes_results_patcher.start()
        self.addCleanup(writes_results_patcher.stop)
        moves_mouse_patcher = patch.object(
            MovesMouse,
            '__init__',
            return_value=MagicMock()
        )
        self.mock_moves_mouse = moves_mouse_patcher.start()
        self.addCleanup(moves_mouse_patcher.stop)
        self.runner = None

    def wipe_runner(self):
        del self.runner

    def construct_runner(self):

        self.runner = RunsComparisons()
        self.addCleanup(self.wipe_runner)


class ConstructorUnitTests(RunsComparisonsTestCase):

    def test_super_calls(self):
        self.construct_runner()
        self.assertEquals(self.mock_writes_results.call_count, 1)
        self.assertEquals(self.mock_moves_mouse.call_count, 1)
