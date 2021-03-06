# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import MagicMock, patch

from wotw_x11_comparison.pointer_window import XlibPointerWindow


class XlibPointerWindowTestCase(TestCase):
    ROOT_WINDOW = 14
    CHILD_WINDOW = 77
    PRIMARY = MagicMock()
    SECONDARY = MagicMock()

    WM_NAME = 'qqq'
    WM_ICON_NAME = 'zzz'

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
        cdll_patcher = patch(
            'wotw_x11_comparison.pointer_window.using_xlib.CDLL',
            return_value=MagicMock()
        )
        self.mock_cdll = cdll_patcher.start()
        self.addCleanup(cdll_patcher.stop)
        xlib_patcher = patch(
            'wotw_x11_comparison.pointer_window.using_xlib.xlib',
            return_value=MagicMock()
        )
        self.mock_xlib = xlib_patcher.start()
        self.addCleanup(xlib_patcher.stop)
        x_open_display_patcher = patch(
            'wotw_x11_comparison.pointer_window.using_xlib.xlib.XOpenDisplay',
            return_value=self.PRIMARY)
        self.mock_x_open_display = x_open_display_patcher.start()
        self.addCleanup(x_open_display_patcher.stop)
        x_default_screen_patcher = patch(
            'wotw_x11_comparison.pointer_window.using_xlib.xlib.XDefaultScreen',
            return_value=self.SECONDARY
        )
        self.mock_x_default_screen = x_default_screen_patcher.start()
        self.addCleanup(x_default_screen_patcher.stop)
        self.window = XlibPointerWindow()
        self.addCleanup(self.wipe_window)


class GatherBasicsUnitTests(XlibPointerWindowTestCase):

    def test_results(self):
        primary, secondary = self.window.gather_basics()
        self.assertEquals(primary, self.PRIMARY)
        self.assertEquals(secondary, self.SECONDARY)


class GetRootWindowUnitTests(XlibPointerWindowTestCase):

    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.xlib.XRootWindow',
        return_value=XlibPointerWindowTestCase.ROOT_WINDOW
    )
    def test_result(self, mock_get):
        self.assertEquals(
            self.ROOT_WINDOW,
            self.window.get_root_window(self.PRIMARY, self.SECONDARY)
        )


class GetMouseWindowsUnitTests(XlibPointerWindowTestCase):

    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.xlib.XQueryPointer'
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.Window',
        return_value=MagicMock(
            value=XlibPointerWindowTestCase.CHILD_WINDOW
        )
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.Coordinate'
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.byref'
    )
    def test_calls(self, mock_byref, mock_coord, mock_window, mock_query):
        mock_holder = MagicMock()
        mock_holder.attach_mock(mock_window, 'Window')
        mock_holder.attach_mock(mock_coord, 'Coordinate')
        mock_holder.attach_mock(mock_byref, 'byref')
        mock_holder.attach_mock(mock_query, ' XQueryPointer')
        root, current = self.window.get_mouse_windows(
            self.PRIMARY,
            self.CHILD_WINDOW
        )
        self.assertEquals(root, current)
        self.assertEquals(mock_window.call_count, 2)
        self.assertEquals(mock_coord.call_count, 4)
        self.assertEquals(mock_byref.call_count, 7)


class GetWindowNamesUnitTests(XlibPointerWindowTestCase):

    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.c_char_p',
        return_value=MagicMock(value=XlibPointerWindowTestCase.WM_NAME)
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.xlib.XFetchName'
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.XTextProperty',
        return_value=MagicMock(value=XlibPointerWindowTestCase.WM_ICON_NAME)
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.xlib.XGetWMIconName'
    )
    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.byref'
    )
    def test_results(self, mock_byref, mock_icon_name, mock_prop, mock_name, mock_char):
        wm_name, wm_icon_name = self.window.get_window_names(
            self.PRIMARY,
            self.ROOT_WINDOW
        )
        self.assertEquals(wm_name, self.WM_NAME)
        self.assertEquals(wm_icon_name, self.WM_ICON_NAME)


class GracefullyExitXUnitTests(XlibPointerWindowTestCase):

    @patch(
        'wotw_x11_comparison.pointer_window.using_xlib.xlib.XCloseDisplay'
    )
    def test_result(self, mock_close):
        self.window.gracefully_exit_x(self.PRIMARY)
        mock_close.assert_called_once_with(self.PRIMARY)
