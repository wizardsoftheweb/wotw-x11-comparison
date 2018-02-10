# pylint: disable=W,C,R

from struct import unpack
from xcb import connect
from xcb.xproto import Atom, GetPropertyReply, GetPropertyType

from wotw_x11_comparison.pointer_window import BasePointerWindow


class XcbPointerWindow(BasePointerWindow):

    def get_property_value(self, reply):
        self.logger.debug("Attempting to parse %s's value", reply)
        if isinstance(reply, GetPropertyReply):
            if 8 == reply.format:
                value = ''
                for chunk in reply.value:
                    value += chr(chunk)
                self.logger.silly("Parsed %s", value)
                return value
            elif reply.format in (16, 32):
                value = list(
                    unpack(
                        'I' * reply.value_len,
                        reply.value.buf()
                    )
                )
                self.logger.silly("Parsed %s", value)
                return value

        self.logger.warning("The reply might not be valid: %s", reply)
        return None

    def get_window_property(self, connection, window, atom):
        self.logger.debug("Getting property %s from window %s", atom, window)
        cookie = connection.core.GetProperty(
            False,
            window,
            atom,
            GetPropertyType.Any,
            0,
            2 ** 32 - 1
        )
        reply = cookie.reply()
        return self.get_property_value(reply)

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
