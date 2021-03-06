# pylint: disable=missing-docstring
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from xcffib.xproto import GetPropertyType

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
    BUFFER_VALUE = MagicMock(buf=MagicMock(return_value=STRING_RESULT))

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
        'wotw_x11_comparison.common.uses_xcb_window_properties.isinstance',
        return_value=True
    )
    def test_buffered_string_property(self, mock_is):
        reply = MagicMock(format=8, value=self.BUFFER_VALUE)
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


class GetWindowPropertyUnitTests(UsesXcbWindowPropertiesTestCase):
    WINDOW = 13
    ATOM = 47

    @patch.object(
        UsesXcbWindowProperties,
        'get_property_value',
        return_value=MagicMock()
    )
    def test_cookie(self, mock_prop):
        mock_get = MagicMock()
        dummy_core = MagicMock(GetProperty=mock_get)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_window_property(
            dummy_connection,
            self.WINDOW,
            self.ATOM
        )
        mock_get.assert_has_calls([
            call(
                False,
                self.WINDOW,
                self.ATOM,
                GetPropertyType.Any,
                0,
                2 ** 32 - 1
            ),
            call().reply()
        ])

    @patch.object(
        UsesXcbWindowProperties,
        'get_property_value',
        return_value=MagicMock()
    )
    def test_get_prop(self, mock_prop):
        mock_get = MagicMock()
        dummy_core = MagicMock(GetProperty=mock_get)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_window_property(
            dummy_connection,
            self.WINDOW,
            self.ATOM
        )
        mock_prop.assert_called_once()


class GetUnknownAtomUnitTests(UsesXcbWindowPropertiesTestCase):
    ATOM = 'WM_NAME'

    def test_existing_only(self):
        mock_intern = MagicMock()
        dummy_core = MagicMock(InternAtom=mock_intern)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_unknown_atom(
            dummy_connection,
            self.ATOM,
            True
        )
        mock_intern.assert_has_calls([
            call(
                True,
                len(self.ATOM),
                self.ATOM
            ),
            call().reply()
        ])

    def test_existing_and_nonexistent(self):
        mock_intern = MagicMock()
        dummy_core = MagicMock(InternAtom=mock_intern)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_unknown_atom(
            dummy_connection,
            self.ATOM
        )
        mock_intern.assert_has_calls([
            call(
                False,
                len(self.ATOM),
                self.ATOM
            ),
            call().reply()
        ])


class GetWindowGeometryUnitTests(UsesXcbWindowPropertiesTestCase):
    WINDOW = 47

    def test_geometry_call(self):
        mock_get = MagicMock()
        dummy_core = MagicMock(GetGeometry=mock_get)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_window_geometry(
            dummy_connection,
            self.WINDOW
        )
        mock_get.assert_has_calls([
            call(
                self.WINDOW
            ),
            call().reply()
        ])


class GetPointerPositionUnitTests(UsesXcbWindowPropertiesTestCase):
    WINDOW = 47

    def test_geometry_call(self):
        mock_query = MagicMock()
        dummy_core = MagicMock(QueryPointer=mock_query)
        dummy_connection = MagicMock(core=dummy_core)
        self.prop_user.get_pointer_position(
            dummy_connection,
            self.WINDOW
        )
        mock_query.assert_has_calls([
            call(self.WINDOW).reply()
        ])
