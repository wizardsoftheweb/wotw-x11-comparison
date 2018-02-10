# pylint: disable=W,C,R

from xcb import connect
from xcb.xproto import Atom

from wotw_x11_comparison.common import UsesXcbWindowProperties
from wotw_x11_comparison.pointer_window import BasePointerWindow


class XcbPointerWindow(UsesXcbWindowProperties, BasePointerWindow):

    library = 'xcb'

    def gather_basics(self):
        self.logger.info('Gathering X connection')
        connection = connect()
        self.logger.debug("Connection: %s", connection)
        setup = connection.get_setup()
        self.logger.debug("Setup: %s", setup)
        return [connection, setup]

    def get_root_window(self, lib_primary, lib_secondary):
        self.logger.debug('Discovering the root window')
        return lib_secondary.roots[0].root

    def get_mouse_windows(self, lib_primary, window):
        cookie = lib_primary.core.QueryPointer(window)
        reply = cookie.reply()
        return [reply.root, reply.child]

    def get_window_names(self, lib_primary, window):
        self.logger.debug("Naming window %s", window)
        wm_name = self.get_window_property(
            lib_primary,
            window,
            Atom.WM_NAME
        )
        self.logger.silly("WM Name: %s", wm_name)
        wm_icon_name = self.get_window_property(
            lib_primary,
            window,
            Atom.WM_ICON_NAME
        )
        self.logger.silly("WM Icon Name: %s", wm_icon_name)
        return [wm_name, wm_icon_name]
