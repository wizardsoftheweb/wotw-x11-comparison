# pylint: disable=missing-docstring,unused-argument,invalid-name,no-self-use
from __future__ import print_function

from unittest import TestCase

# from mock import call, MagicMock, patch
from mock import MagicMock, patch

# from wotw_x11_comparison.common import HasLogger
from wotw_x11_comparison.common import UsesXcbWindowProperties


class UsesXcbWindowPropertiesTestCase(TestCase):

    def setUp(self):
        self.construct_prop_user()

    def wipe_prop_user(self):
        del self.prop_user

    def construct_prop_user(self):
        has_logger_patcher = patch(
            'wotw_x11_comparison.common.has_logger.getLogger',
            return_value=MagicMock()
        )
        self.mock_has_logger = has_logger_patcher.start()
        self.addCleanup(has_logger_patcher.stop)
        self.prop_user = UsesXcbWindowProperties()
        self.addCleanup(self.wipe_prop_user)


class GetPropertyValueUnitTests(UsesXcbWindowPropertiesTestCase):
    REPLY = MagicMock()
    # VALUE = [68, 101, 108, 117, 103, 101]
    STRING_VALUE = [83, 117, 98, 108, 105, 109, 101, 32, 84, 101, 120, 116]
    STRING_RESULT = 'Sublime Text'
    ARRAY_VALUE = [1, 2, 3]

    # def setUp(self):
    #     isinstance_patcher = patch('')
    #     self.mock_isinstance = isinstance_patcher.start()
    #     self.addCleanup(isinstance_patcher.stop)

    @patch(
        'wotw_x11_comparison.common.uses_xcb_window_properties.isinstance',
        return_value=False
    )
    def test_not_a_reply(self, mock_is):
        self.assertIsNone(self.prop_user.get_property_value(self.REPLY))

    @patch(
        'wotw_x11_comparison.common.uses_xcb_window_properties.isinstance',
        return_value=True
    )
    def test_string_property(self, mock_is):
        reply = MagicMock(format=8, value=self.STRING_VALUE)
        self.assertEquals(
            self.STRING_RESULT,
            self.prop_user.get_property_value(reply)
        )

    @patch(
        'wotw_x11_comparison.common.uses_xcb_window_properties.unpack',
        return_value=ARRAY_VALUE
    )
    @patch(
        'wotw_x11_comparison.common.uses_xcb_window_properties.isinstance',
        return_value=True
    )
    def test_array_property(self, mock_is, mock_unpack):
        reply = MagicMock(format=16, value=MagicMock())
        self.assertEquals(
            self.ARRAY_VALUE,
            self.prop_user.get_property_value(reply)
        )
