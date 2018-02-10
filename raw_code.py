# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

from ctypes import *

xcb = CDLL('libxcb.so.1')

DisplayName = c_char_p
ScreenNumber = c_int


class xcb_connection_t(Structure):
    _fields_ = [
        ('_opaque_struct', c_int)
    ]

xcb.xcb_connect.argtypes = [DisplayName, POINTER(ScreenNumber)]
xcb.xcb_connect.restype = xcb_connection_t

DEFAULT_SCREEN_NUMBER = ScreenNumber()
CONNECTION = xcb.xcb_connect(None, byref(DEFAULT_SCREEN_NUMBER))
print(CONNECTION)
print(DEFAULT_SCREEN_NUMBER)
