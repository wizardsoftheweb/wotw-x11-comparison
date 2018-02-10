# pylint: disable=missing-docstring,unused-argument,invalid-name
# pylint: disable=no-self-use,protected-access,unused-import,too-many-arguments
from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_x11_comparison.pointer_window import PointerWindowComparison


class PointerWindowComparisonTestCase(TestCase):
    ROOT_WINDOW = 14
    CHILD_WINDOW = 77
    ROOTS = [MagicMock(root=ROOT_WINDOW)]
    SECONDARY = MagicMock(roots=ROOTS)
    QUERY_POINTER_REPLY = MagicMock(
        return_value=[ROOT_WINDOW, CHILD_WINDOW]
    )
    QUERY_POINTER = MagicMock(reply=QUERY_POINTER_REPLY)
    PRIMARY = MagicMock(
        core=MagicMock(QueryPointer=QUERY_POINTER),
        get_setup=MagicMock(return_value=SECONDARY)
    )
    POSITION = MagicMock(
        root_x=0,
        root_y=1,
        win_x=2,
        win_y=3
    )
    RUN_TIME = 0.314

    WM_NAME = 'qqq'

    def setUp(self):
        self.runner = PointerWindowComparison()
        self.addCleanup(self.wipe_runner)

    def wipe_runner(self):
        del self.runner


class RunSingleTrialOneLibraryUnitTests(PointerWindowComparisonTestCase):
    LIBRARY = 'xcb'
    POINTER_WINDOW = MagicMock(library=LIBRARY)

    @patch(
        'wotw_x11_comparison.pointer_window.runner.connect',
        return_value=PointerWindowComparisonTestCase.PRIMARY
    )
    @patch.object(
        PointerWindowComparison,
        'warp_to_random_window',
        return_value=PointerWindowComparisonTestCase.CHILD_WINDOW
    )
    @patch.object(
        PointerWindowComparison,
        'get_pointer_position',
        return_value=PointerWindowComparisonTestCase.POSITION
    )
    @patch.object(
        PointerWindowComparison,
        'benchmark',
        return_value=PointerWindowComparisonTestCase.RUN_TIME
    )
    @patch.object(
        PointerWindowComparison,
        'write_result_row',
    )
    def test_results(
            self,
            mock_write,
            mock_benchmark,
            mock_pointer,
            mock_warp,
            mock_connect
    ):
        self.runner.run_single_trial_one_library(self.POINTER_WINDOW)
        expected = {
            'library': self.LIBRARY,
            'time': PointerWindowComparisonTestCase.RUN_TIME,
            'root_x': 0,
            'root_y': 1,
            'window': PointerWindowComparisonTestCase.CHILD_WINDOW,
            'win_x': 2,
            'win_y': 3,
        }
        mock_write.assert_called_once_with(expected)


class RunSingleTrialAllLibrariesUnitTests(PointerWindowComparisonTestCase):
    LIBRARY_ONE = MagicMock
    LIBRARY_TWO = MagicMock
    LIBRARY_THREE = MagicMock
    LIBRARIES = [LIBRARY_ONE, LIBRARY_TWO, LIBRARY_THREE]

    @patch.object(
        PointerWindowComparison,
        'run_single_trial_one_library',
    )
    def test_results(self, mock_run):
        self.runner.LIBRARIES = self.LIBRARIES
        self.runner.run_single_trial_all_libraries()
        self.assertEquals(
            len(self.LIBRARIES),
            mock_run.call_count
        )


class RunManyTrialsUnitTests(PointerWindowComparisonTestCase):
    RUN_COUNT = 15

    @patch.object(
        PointerWindowComparison,
        'run_single_trial_all_libraries',
    )
    def test_results_with_base_run_count(self, mock_run):
        self.runner.run_many_trials()
        self.assertEquals(
            PointerWindowComparison.RUN_COUNT,
            mock_run.call_count
        )

    @patch.object(
        PointerWindowComparison,
        'run_single_trial_all_libraries',
    )
    def test_results_with_new_run_count(self, mock_run):
        self.runner.run_many_trials(self.RUN_COUNT)
        self.assertEquals(
            self.RUN_COUNT,
            mock_run.call_count
        )
