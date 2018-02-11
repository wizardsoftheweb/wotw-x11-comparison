# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wotw_x11_comparison.pointer_window import BasePointerWindow


class SimpleWindow(BasePointerWindow):
    RANDOM_WINDOW = 100
    ROOT_WINDOW = 50
    SAFE_WINDOW = 10
    CHILD_WINDOW = 1
    NO_CHILDREN = 0
    SAME_WINDOW = 5
    PRIMARY = MagicMock()
    SECONDARY = MagicMock()
    WM_NAME = 'rad'
    WM_ICON_NAME = None

    def gather_basics(self):
        return [self.PRIMARY, self.SECONDARY]

    def get_root_window(self, lib_primary, lib_secondary):
        return self.ROOT_WINDOW

    def get_mouse_windows(self, lib_primary, window):
        if self.SAFE_WINDOW == window:
            return [self.ROOT_WINDOW, self.CHILD_WINDOW]
        elif self.SAME_WINDOW == window:
            return [self.ROOT_WINDOW, self.ROOT_WINDOW]
        return [self.ROOT_WINDOW, 0]

    def get_window_names(self, lib_primary, window):
        return [self.WM_NAME, self.WM_ICON_NAME]

    def gracefully_exit_x(self, lib_primary):
        pass


class BasePointerWindowTestCase(TestCase):
    PRIMARY = MagicMock()

    def setUp(self):
        self.construct_window()

    def wipe_window(self):
        del self.window

    def construct_window(self):
        has_logger_patcher = patch(
            'wotw_x11_comparison.common.has_logger.getLogger',
            return_value=MagicMock()
        )
        self.mock_has_logger = has_logger_patcher.start()
        self.addCleanup(has_logger_patcher.stop)
        self.window = SimpleWindow()
        self.addCleanup(self.wipe_window)


class GetWindowUnderPointerUnitTests(BasePointerWindowTestCase):

    def test_childless_window(self):
        result = self.window.get_window_under_pointer(
            self.PRIMARY,
            SimpleWindow.NO_CHILDREN
        )
        self.assertEquals(SimpleWindow.NO_CHILDREN, result)

    def test_window_with_child(self):
        result = self.window.get_window_under_pointer(
            self.PRIMARY,
            SimpleWindow.SAFE_WINDOW
        )
        self.assertEquals(SimpleWindow.CHILD_WINDOW, result)

    def test_same_window(self):
        result = self.window.get_window_under_pointer(
            self.PRIMARY,
            SimpleWindow.SAME_WINDOW
        )
        self.assertEquals(SimpleWindow.SAME_WINDOW, result)

    def test_bad_window(self):
        result = self.window.get_window_under_pointer(
            self.PRIMARY,
            SimpleWindow.RANDOM_WINDOW
        )
        self.assertEquals(SimpleWindow.RANDOM_WINDOW, result)


class ParseNamesUnitTests(BasePointerWindowTestCase):
    EMPTY_NAME = None
    SHORT_NAME = 'qqq'
    LONG_NAME = 'abacus'
    FIRST_SIMILAR_NAME = 'cool'
    SECOND_SIMILAR_NAME = 'yeah'
    FIRST_NAMES = [
        EMPTY_NAME,
        EMPTY_NAME,
        FIRST_SIMILAR_NAME,
        FIRST_SIMILAR_NAME,
        SHORT_NAME,
        LONG_NAME
    ]
    SECOND_NAMES = [
        EMPTY_NAME,
        SECOND_SIMILAR_NAME,
        EMPTY_NAME,
        SECOND_SIMILAR_NAME,
        LONG_NAME,
        SHORT_NAME
    ]
    RESULTS = [
        '',
        SECOND_SIMILAR_NAME,
        FIRST_SIMILAR_NAME,
        FIRST_SIMILAR_NAME,
        LONG_NAME,
        LONG_NAME
    ]

    def test_everything(self):
        for index in range(0, len(self.RESULTS)):
            print(index)
            self.assertEquals(
                self.window.parse_names(
                    self.FIRST_NAMES[index],
                    self.SECOND_NAMES[index]
                ),
                self.RESULTS[index]
            )


class FindWindowUnitTests(BasePointerWindowTestCase):

    @patch.object(
        SimpleWindow,
        'parse_names',
        return_value=SimpleWindow.WM_NAME
    )
    @patch.object(
        SimpleWindow,
        'get_window_under_pointer',
        return_value=SimpleWindow.CHILD_WINDOW
    )
    def test_result(self, mock_get, mock_parse):
        window, wm_name, timing = self.window.find_window()
        self.assertEquals(window, SimpleWindow.CHILD_WINDOW)
        self.assertEquals(wm_name, SimpleWindow.WM_NAME)
        self.assertEquals(len(timing), 7)
