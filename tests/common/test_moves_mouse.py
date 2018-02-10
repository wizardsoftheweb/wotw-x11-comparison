# pylint: disable=missing-docstring
# pylint: disable=protected-access
# pylint: disable=unused-argument

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from xcb.xproto import Atom

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


class MoveToRandomPositionInWindowUnitTests(MovesMouseTestCase):
    RANDOM_INT = 2
    WINDOW = 99

    @patch(
        'wotw_x11_comparison.common.moves_mouse.randint',
        return_value=RANDOM_INT
    )
    def test_warp_pointer(self, mock_rand):
        mock_warp = MagicMock()
        dummy_core = MagicMock(WarpPointer=mock_warp)
        mock_flush = MagicMock()
        dummy_connection = MagicMock(core=dummy_core, flush=mock_flush)
        mock_holder = MagicMock()
        mock_holder.attach_mock(
            self.mock_get_window_geometry,
            'get_window_geometry'
        )
        mock_holder.attach_mock(
            mock_warp,
            'WarpPointer'
        )
        mock_holder.attach_mock(
            mock_rand,
            'randint'
        )
        mock_holder.attach_mock(
            mock_flush,
            'flush'
        )
        self.mover.move_to_random_position_in_window(
            dummy_connection,
            self.WINDOW
        )
        mock_holder.assert_has_calls([
            call.get_window_geometry(dummy_connection, self.WINDOW),
            call.randint(0, self.WIDTH),
            call.randint(0, self.HEIGHT),
            call.WarpPointer(
                Atom._None,
                self.WINDOW,
                0,
                0,
                0,
                0,
                self.RANDOM_INT,
                self.RANDOM_INT
            ),
            call.flush()
        ])


class WarpToRandomWindowUnitTests(MovesMouseTestCase):
    WINDOW = 24
    ROOT_WINDOW = 17

    @patch.object(
        MovesMouse,
        'choose_a_random_window',
        return_value=WINDOW
    )
    @patch.object(
        MovesMouse,
        'move_to_random_position_in_window'
    )
    def test_full_warp(self, mock_move, mock_choose):
        mock_holder = MagicMock()
        mock_holder.attach_mock(
            mock_choose,
            'choose_a_random_window'
        )
        mock_holder.attach_mock(
            mock_move,
            'move_to_random_position_in_window'
        )
        connection = MagicMock()
        self.mover.warp_to_random_window(connection, self.ROOT_WINDOW)
        mock_holder.assert_has_calls([
            call.choose_a_random_window(connection, self.ROOT_WINDOW),
            call.move_to_random_position_in_window(connection, self.WINDOW)
        ])
