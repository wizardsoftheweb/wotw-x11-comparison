"""This file provides UsesXcbWindowProperties"""

from struct import unpack
from xcb.xproto import GetPropertyReply, GetPropertyType

from wotw_x11_comparison.common import HasLogger


class UsesXcbWindowProperties(HasLogger):
    """This class collects several useful XCB window tools"""

    def __init__(self, *args, **kwargs):
        super(UsesXcbWindowProperties, self).__init__(*args, **kwargs)

    def get_property_value(self, reply):
        """
        Parses the property's value.
        @see https://bbs.archlinux.org/viewtopic.php?pid=891853#p891853
        """
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
        """Gets an atomized window property"""
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

    @staticmethod
    def get_unknown_atom(connection, atom, exists_only=False):
        """Finds the number for an unknown atom"""
        cookie = connection.core.InternAtom(
            exists_only,
            len(atom),
            atom
        )
        reply = cookie.reply()
        return reply.atom

    @staticmethod
    def get_window_geometry(connection, window):
        """Gets the window geometry"""
        cookie = connection.core.GetGeometry(window)
        return cookie.reply()

    @staticmethod
    def get_pointer_position(connection, window):
        """Gets the pointer position"""
        return connection.core.QueryPointer(window).reply()
