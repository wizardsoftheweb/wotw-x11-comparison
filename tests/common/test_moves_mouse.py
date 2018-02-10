# pylint: disable=missing-docstring,unused-argument,invalid-name,no-self-use
from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
# from xcb.xproto import GetPropertyType

from wotw_x11_comparison.common import MovesMouse


class MovesMouseTestCase(TestCase):
    UNKNOWN_ATOM = 13
    LIST_OF_WINDOWS = [1, 2, 3]
    WIDTH = 42
    HEIGHT = 37

    def setUp(self):
        self.construct_mover()

    def wipe_mover(self):
        del self.mover

    def construct_mover(self):
        self.mover = MovesMouse()
        get_unknown_atom_patcher = patch.object(
            MovesMouse,
            'get_unknown_atom',
            return_value=self.UNKNOWN_ATOM
        )
        self.mock_get_unknown_atom = get_unknown_atom_patcher.start()
        self.addCleanup(get_unknown_atom_patcher.stop)
        get_window_property_patcher = patch.object(
            MovesMouse,
            'get_window_property',
            return_value=self.LIST_OF_WINDOWS
        )
        self.mock_get_window_property = get_window_property_patcher.start()
        self.addCleanup(get_window_property_patcher.stop)
        get_window_geometry_patcher = patch.object(
            MovesMouse,
            'get_window_geometry',
            return_value=MagicMock(width=self.WIDTH, height=self.HEIGHT)
        )
        self.mock_get_window_geometry = get_window_geometry_patcher.start()
        self.addCleanup(get_window_geometry_patcher.stop)
        self.addCleanup(self.wipe_mover)


class ChooseARandomWindowUnitTests(MovesMouseTestCase):
    RANDOM_INT = 2
    WINDOW = 99

    @patch(
        'wotw_x11_comparison.common.moves_mouse.randint',
        return_value=RANDOM_INT
    )
    def test_prop_calls(self, mock_rand):
        mock_holder = MagicMock()
        mock_holder.attach_mock(
            self.mock_get_unknown_atom,
            'get_unknown_atom'
        )
        mock_holder.attach_mock(
            self.mock_get_window_property,
            'get_window_property'
        )
        mock_holder.attach_mock(
            mock_rand,
            'randint'
        )
        connection = MagicMock()
        self.mover.choose_a_random_window(connection, self.WINDOW)
        mock_holder.assert_has_calls([
            call.get_unknown_atom(connection, '_NET_CLIENT_LIST'),
            call.get_window_property(
                connection, self.WINDOW, self.UNKNOWN_ATOM),
            call.randint(0, len(self.LIST_OF_WINDOWS) - 1)
        ])

    @patch(
        'wotw_x11_comparison.common.moves_mouse.randint',
        return_value=RANDOM_INT
    )
    def test_random_result(self, mock_rand):
        connection = MagicMock()
        result = self.mover.choose_a_random_window(connection, self.WINDOW)
        self.assertEquals(
            self.LIST_OF_WINDOWS[self.RANDOM_INT],
            result
        )
