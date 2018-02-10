# pylint: disable=missing-docstring,unused-argument,invalid-name
# pylint: disable=no-self-use,protected-access,unused-import
from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_x11_comparison.pointer_window import BasePointerWindow


class SimpleWindow(BasePointerWindow):
    RANDOM_WINDOW = 100
    ROOT_WINDOW = 50
    SAFE_WINDOW = 10
    CHILD_WINDOW = 1
    NO_CHILDREN = 0
    SAME_WINDOW = 5

    def gather_basics(self):
        pass

    def get_root_window(self, lib_primary, lib_secondary):
        pass

    def get_mouse_windows(self, lib_primary, window):
        if self.SAFE_WINDOW == window:
            return [self.ROOT_WINDOW, self.CHILD_WINDOW]
        elif self.SAME_WINDOW == window:
            return [self.ROOT_WINDOW, self.ROOT_WINDOW]
        return [self.ROOT_WINDOW, 0]

    def get_window_names(self, lib_primary, window):
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
