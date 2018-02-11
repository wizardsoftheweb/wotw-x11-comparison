# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

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
    DISCONNECT = MagicMock()
    PRIMARY = MagicMock(
        core=MagicMock(QueryPointer=QUERY_POINTER),
        disconnect=DISCONNECT,
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
    POINTER_WINDOW = MagicMock(
        return_value=MagicMock(
            library=LIBRARY,
            find_window=MagicMock(
                return_value=[
                    PointerWindowComparisonTestCase.CHILD_WINDOW,
                    PointerWindowComparisonTestCase.WM_NAME,
                    [
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME,
                        PointerWindowComparisonTestCase.RUN_TIME
                    ]
                ]
            )
        )
    )

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
    @patch(
        'wotw_x11_comparison.pointer_window.base.time_now',
        return_value=PointerWindowComparisonTestCase.RUN_TIME
    )
    @patch.object(
        PointerWindowComparison,
        'write_result_row',
    )
    def test_results(
            self,
            mock_write,
            mock_time,
            mock_pointer,
            mock_warp,
            mock_connect
    ):
        self.runner.run_single_trial_one_library(self.POINTER_WINDOW)
        expected = {
            'library': self.LIBRARY,
            'root_x': 0,
            'root_y': 1,
            'window': PointerWindowComparisonTestCase.CHILD_WINDOW,
            'win_x': 2,
            'win_y': 3,
            'start': PointerWindowComparisonTestCase.RUN_TIME,
            'gather_basics': PointerWindowComparisonTestCase.RUN_TIME,
            'root_window': PointerWindowComparisonTestCase.RUN_TIME,
            'recursion': PointerWindowComparisonTestCase.RUN_TIME,
            'get_names': PointerWindowComparisonTestCase.RUN_TIME,
            'parse_names': PointerWindowComparisonTestCase.RUN_TIME,
            'exit': PointerWindowComparisonTestCase.RUN_TIME
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
