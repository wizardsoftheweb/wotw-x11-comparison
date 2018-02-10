# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

from ctypes import *

xcb = CDLL('libxcb.so.1')

int16_t = c_int16
uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32

DisplayName = c_char_p
ScreenNumber = c_int

IGNORED_FOR_NOW = POINTER(c_int)


class xcb_generic_error_t(Structure):
    _fields_ = [
        ('response_type', uint8_t),
        ('error_code', uint8_t),
        ('sequence', uint16_t),
        ('resource_id', uint32_t),
        ('minor_code', uint16_t),
        ('major_code', uint8_t),
        ('pad0', uint8_t),
        ('pad', uint32_t * 5),
        ('full_sequence', uint32_t),
    ]


class xcb_connection_t(Structure):
    _fields_ = [
        ('_opaque_struct', c_int)
    ]

xcb_window_t = c_ulong


class xcb_setup_t(Structure):
    _fields_ = [
        ('status', uint8_t),
        ('pad0', uint8_t),
        ('protocol_major_version', uint16_t),
        ('protocol_minor_version', uint16_t),
        ('length', uint16_t),
        ('release_number', uint32_t),
        ('resource_id_base', uint32_t),
        ('resource_id_mask', uint32_t),
        ('motion_buffer_size', uint32_t),
        ('vendor_len', uint16_t),
        ('maximum_request_length', uint16_t),
        ('roots_len', uint8_t),
        ('pixmap_formats_len', uint8_t),
        ('image_byte_order', uint8_t),
        ('bitmap_format_bit_order', uint8_t),
        ('bitmap_format_scanline_unit', uint8_t),
        ('bitmap_format_scanline_pad', uint8_t),
        ('min_keycode', IGNORED_FOR_NOW),
        ('max_keycode', IGNORED_FOR_NOW),
        ('pad1', uint8_t * 4),
    ]


class xcb_screen_t(Structure):
    _fields_ = [
        ('root', xcb_window_t),
        ('default_colormap', IGNORED_FOR_NOW),
        ('white_pixel', uint32_t),
        ('black_pixel', uint32_t),
        ('current_input_masks', uint32_t),
        ('width_in_pixels', uint16_t),
        ('height_in_pixels', uint16_t),
        ('width_in_millimeters', uint16_t),
        ('height_in_millimeters', uint16_t),
        ('min_installed_maps', uint16_t),
        ('max_installed_maps', uint16_t),
        ('root_visual', IGNORED_FOR_NOW),
        ('backing_stores', uint8_t),
        ('save_unders', uint8_t),
        ('root_depth', uint8_t),
        ('allowed_depths_len', uint8_t),
    ]


class xcb_screen_iterator_t(Structure):
    _fields_ = [
        ('data', POINTER(xcb_screen_t)),
        ('rem', uint8_t),
        ('index', uint8_t),
    ]


def screen_of_display(xcb_connection, xcb_screen_number):
    # https://xcb.freedesktop.org/xlibtoxcbtranslationguide/#screenofdisplay
    try:
        screen = xcb_screen_number.value
    except AttributeError:
        screen = xcb_screen_number
    setup = xcb.xcb_get_setup(xcb_connection)
    iterator = xcb.xcb_setup_roots_iterator(setup)
    while iterator.rem:
        if 0 == screen:
            return iterator.data
        screen -= 1
        xcb.xcb_screen_next(iterator)
    return None


class xcb_query_pointer_cookie_t(Structure):
    _fields_ = [
        ('sequence', c_uint)
    ]


# class xcb_query_pointer_request_t(Structure):
#     _fields_ = [
#         ('major_opcode', uint8_t),
#         ('pad0', uint8_t),
#         ('length', uint16_t),
#         ('window', xcb_window_t),
#     ]

class xcb_query_pointer_reply_t(Structure):
    _fields_ = [
        ('response_type', uint8_t),
        ('same_screen', uint8_t),
        ('sequence', uint16_t),
        ('length', uint32_t),
        ('root', xcb_window_t),
        ('child', xcb_window_t),
        ('root_x', int16_t),
        ('root_y', int16_t),
        ('win_x', int16_t),
        ('win_y', int16_t),
        ('mask', uint16_t),
        ('pad0', uint8_t * 2)
    ]

xcb.xcb_connect.argtypes = [DisplayName, POINTER(ScreenNumber)]
xcb.xcb_connect.restype = POINTER(xcb_connection_t)
xcb.xcb_get_setup.argtypes = [POINTER(xcb_connection_t)]
xcb.xcb_get_setup.restype = POINTER(xcb_setup_t)
xcb.xcb_setup_roots_iterator.argtypes = [POINTER(xcb_setup_t)]
xcb.xcb_setup_roots_iterator.restype = xcb_screen_iterator_t
xcb.xcb_screen_next.argtypes = [POINTER(xcb_screen_iterator_t)]
xcb.xcb_screen_next.restype = None
xcb.xcb_query_pointer.argtypes = [POINTER(xcb_connection_t), xcb_window_t]
xcb.xcb_query_pointer.restype = xcb_query_pointer_cookie_t

DEFAULT_SCREEN_NUMBER = ScreenNumber()
CONNECTION = xcb.xcb_connect(None, byref(DEFAULT_SCREEN_NUMBER))
DEFAULT_SCREEN = screen_of_display(CONNECTION, DEFAULT_SCREEN_NUMBER)
ROOT_WINDOW = DEFAULT_SCREEN.contents.root
COOKIE = xcb.xcb_query_pointer(CONNECTION, ROOT_WINDOW)
print(COOKIE.sequence)
