"""This file provides XcbPointerWindow"""

from xcffib import connect
from xcffib.xproto import Atom

from wotw_x11_comparison.common import UsesXcbWindowProperties
from wotw_x11_comparison.pointer_window import BasePointerWindow


class XcbPointerWindow(UsesXcbWindowProperties, BasePointerWindow):
    """
    This class uses XCB to determine the window beneath the pointer
    """

    library = 'xcb'

    def gather_basics(self):
        """Gets the connection and setup"""
        self.logger.info('Gathering X connection')
        connection = connect()
        self.logger.debug("Connection: %s", connection)
        setup = connection.get_setup()
        self.logger.debug("Setup: %s", setup)
        return [connection, setup]

    def get_root_window(self, lib_primary, lib_secondary):
        """Pulls the root window"""
        self.logger.debug('Discovering the root window')
        return lib_secondary.roots[0].root

    def get_mouse_windows(self, lib_primary, window):
        """Finds the children of window beneath the pointer (if any)"""
        cookie = lib_primary.core.QueryPointer(window)
        reply = cookie.reply()
        return [reply.root, reply.child]

    def get_window_names(self, lib_primary, window):
        """Gets WM_NAME and WM_ICON_NAME for the specified window"""
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

    def gracefully_exit_x(self, lib_primary):
        """Gracefully disconnects from the X server"""
        lib_primary.disconnect()
