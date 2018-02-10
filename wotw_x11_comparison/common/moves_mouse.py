# pylint: disable=W,C,R

from random import randint
from xcb.xproto import Atom

from wotw_x11_comparison.common import UsesXcbWindowProperties


class MovesMouse(UsesXcbWindowProperties):

    def choose_a_random_window(self, connection, root_window):
        _NET_CLIENT_LIST = self.get_unknown_atom(
            connection,
            '_NET_CLIENT_LIST'
        )
        viable_windows = self.get_window_property(
            connection,
            root_window,
            _NET_CLIENT_LIST
        )
        window_index = randint(0, len(viable_windows) - 1)
        return viable_windows[window_index]

    def move_to_random_position_in_window(self, connection, window):
        geometry = self.get_window_geometry(connection, window)
        connection.core.WarpPointer(
            Atom._None,
            window,
            0,
            0,
            0,
            0,
            randint(0, geometry.width),
            randint(0, geometry.height)
        )
        connection.flush()

    def warp_to_random_window(self, connection, root_window):
        window = self.choose_a_random_window(connection, root_window)
        self.move_to_random_position_in_window(connection, window)
        return window
