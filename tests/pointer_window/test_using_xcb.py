# pylint: disable=missing-docstring,unused-argument,invalid-name
# pylint: disable=no-self-use,protected-access,unused-import
from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_x11_comparison.pointer_window import XcbPointerWindow


class XcbPointerWindowTestCase(TestCase):
    ROOT_WINDOW = 14
    ROOTS = [MagicMock(root=ROOT_WINDOW)]
    SECONDARY = MagicMock(roots=ROOTS)

    PRIMARY = MagicMock(get_setup=MagicMock(return_value=SECONDARY))

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
