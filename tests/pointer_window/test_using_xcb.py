# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from xcffib.xproto import Atom

from wotw_x11_comparison.pointer_window import XcbPointerWindow


class XcbPointerWindowTestCase(TestCase):
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

    WM_NAME = 'qqq'

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
        get_window_property_patcher = patch.object(
            XcbPointerWindow,
            'get_window_property',
            return_value=self.WM_NAME
        )
        self.mock_get_window_property = get_window_property_patcher.start()
        self.addCleanup(get_window_property_patcher.stop)
        self.window = XcbPointerWindow()
        self.addCleanup(self.wipe_window)


class GatherBasicsUnitTests(XcbPointerWindowTestCase):

    @patch(
        'wotw_x11_comparison.pointer_window.using_xcb.connect',
        return_value=XcbPointerWindowTestCase.PRIMARY
    )
    def test_results(self, mock_connect):
        primary, secondary = self.window.gather_basics()
        self.assertEquals(primary, self.PRIMARY)
        self.assertEquals(secondary, self.SECONDARY)


class GetRootWindowUnitTests(XcbPointerWindowTestCase):

    def test_results(self):
        self.assertEquals(
            self.ROOT_WINDOW,
            self.window.get_root_window(self.PRIMARY, self.SECONDARY)
        )


class GetMouseWindowsUnitTests(XcbPointerWindowTestCase):

    def test_calls(self):
        mock_holder = MagicMock()
        mock_holder.attach_mock(
            self.QUERY_POINTER,
            'QueryPointer'
        )
        self.window.get_mouse_windows(self.PRIMARY, self.ROOT_WINDOW)
        mock_holder.assert_has_calls([
            call.QueryPointer(self.ROOT_WINDOW),
            call.QueryPointer().reply()
        ])


class GetWindowNamesUnitTests(XcbPointerWindowTestCase):

    def test_calls(self):
        self.window.get_window_names(self.PRIMARY, self.ROOT_WINDOW)
        self.mock_get_window_property.assert_has_calls([
            call(
                self.PRIMARY,
                self.ROOT_WINDOW,
                Atom.WM_NAME
            ),
            call(
                self.PRIMARY,
                self.ROOT_WINDOW,
                Atom.WM_ICON_NAME
            ),
        ])
