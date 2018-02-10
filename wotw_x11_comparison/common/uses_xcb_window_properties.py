# pylint: disable=W,C,R

from struct import unpack
from xcb.xproto import GetPropertyReply, GetPropertyType

from wotw_x11_comparison.common import HasLogger


class UsesXcbWindowProperties(HasLogger):

    def __init__(self, *args, **kwargs):
        super(UsesXcbWindowProperties, self).__init__(*args, **kwargs)

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

    def get_unknown_atom(self, connection, atom, exists_only=False):
        cookie = connection.core.InternAtom(
            exists_only,
            len(atom),
            atom
        )
        reply = cookie.reply()
        return reply.atom

    def get_window_geometry(self, connection, window):
        cookie = connection.core.GetGeometry(window)
        return cookie.reply()

    def get_pointer_position(self, connection, window):
        return connection.core.QueryPointer(window).reply()
