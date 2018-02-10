# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

from ctypes import *

xcb = CDLL('libxcb.so.1')


class GenericCookie(Structure):
    _fields_ = [
        ('sequence', c_uint)
    ]

int16_t = c_int16
uint8_t = c_uint8
uint16_t = c_uint16
uint32_t = c_uint32

DisplayName = c_char_p
ScreenNumber = c_int

XCB_ATOM_NONE = 0
XCB_ATOM_ANY = 0
XCB_ATOM_PRIMARY = 1
XCB_ATOM_SECONDARY = 2
XCB_ATOM_ARC = 3
XCB_ATOM_ATOM = 4
XCB_ATOM_BITMAP = 5
XCB_ATOM_CARDINAL = 6
XCB_ATOM_COLORMAP = 7
XCB_ATOM_CURSOR = 8
XCB_ATOM_CUT_BUFFER0 = 9
XCB_ATOM_CUT_BUFFER1 = 10
XCB_ATOM_CUT_BUFFER2 = 11
XCB_ATOM_CUT_BUFFER3 = 12
XCB_ATOM_CUT_BUFFER4 = 13
XCB_ATOM_CUT_BUFFER5 = 14
XCB_ATOM_CUT_BUFFER6 = 15
XCB_ATOM_CUT_BUFFER7 = 16
XCB_ATOM_DRAWABLE = 17
XCB_ATOM_FONT = 18
XCB_ATOM_INTEGER = 19
XCB_ATOM_PIXMAP = 20
XCB_ATOM_POINT = 21
XCB_ATOM_RECTANGLE = 22
XCB_ATOM_RESOURCE_MANAGER = 23
XCB_ATOM_RGB_COLOR_MAP = 24
XCB_ATOM_RGB_BEST_MAP = 25
XCB_ATOM_RGB_BLUE_MAP = 26
XCB_ATOM_RGB_DEFAULT_MAP = 27
XCB_ATOM_RGB_GRAY_MAP = 28
XCB_ATOM_RGB_GREEN_MAP = 29
XCB_ATOM_RGB_RED_MAP = 30
XCB_ATOM_STRING = 31
XCB_ATOM_VISUALID = 32
XCB_ATOM_WINDOW = 33
XCB_ATOM_WM_COMMAND = 34
XCB_ATOM_WM_HINTS = 35
XCB_ATOM_WM_CLIENT_MACHINE = 36
XCB_ATOM_WM_ICON_NAME = 37
XCB_ATOM_WM_ICON_SIZE = 38
XCB_ATOM_WM_NAME = 39
XCB_ATOM_WM_NORMAL_HINTS = 40
XCB_ATOM_WM_SIZE_HINTS = 41
XCB_ATOM_WM_ZOOM_HINTS = 42
XCB_ATOM_MIN_SPACE = 43
XCB_ATOM_NORM_SPACE = 44
XCB_ATOM_MAX_SPACE = 45
XCB_ATOM_END_SPACE = 46
XCB_ATOM_SUPERSCRIPT_X = 47
XCB_ATOM_SUPERSCRIPT_Y = 48
XCB_ATOM_SUBSCRIPT_X = 49
XCB_ATOM_SUBSCRIPT_Y = 50
XCB_ATOM_UNDERLINE_POSITION = 51
XCB_ATOM_UNDERLINE_THICKNESS = 52
XCB_ATOM_STRIKEOUT_ASCENT = 53
XCB_ATOM_STRIKEOUT_DESCENT = 54
XCB_ATOM_ITALIC_ANGLE = 55
XCB_ATOM_X_HEIGHT = 56
XCB_ATOM_QUAD_WIDTH = 57
XCB_ATOM_WEIGHT = 58
XCB_ATOM_POINT_SIZE = 59
XCB_ATOM_RESOLUTION = 60
XCB_ATOM_COPYRIGHT = 61
XCB_ATOM_NOTICE = 62
XCB_ATOM_FONT_NAME = 63
XCB_ATOM_FAMILY_NAME = 64
XCB_ATOM_FULL_NAME = 65
XCB_ATOM_CAP_HEIGHT = 66
XCB_ATOM_WM_CLASS = 67
XCB_ATOM_WM_TRANSIENT_FOR = 68

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

xcb_atom_t = uint32_t


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

xcb_query_pointer_cookie_t = GenericCookie


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

xcb_get_property_cookie_t = GenericCookie


class xcb_get_property_reply_t(Structure):
    _fields_ = [
        ('response_type', uint8_t),
        ('format', uint8_t),
        ('sequence', uint16_t),
        ('length', uint32_t),
        ('type', xcb_atom_t),
        ('bytes_after', uint32_t),
        ('value_len', uint32_t),
        ('pad0', uint8_t * 12)
    ]

xcb_query_tree_cookie_t = GenericCookie


class xcb_query_tree_reply_t(Structure):
    _fields_ = [
        ('response_type', uint8_t),
        ('pad0', uint8_t),
        ('sequence', uint16_t),
        ('length', uint32_t),
        ('root', xcb_window_t),
        ('parent', xcb_window_t),
        ('children_len', uint16_t),
        ('pad1', uint8_t * 14)
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

xcb.xcb_query_pointer_reply.argtypes = [
    POINTER(xcb_connection_t),
    xcb_query_pointer_cookie_t,
    POINTER(POINTER(xcb_generic_error_t))
]
xcb.xcb_query_pointer_reply.restype = POINTER(xcb_query_pointer_reply_t)

xcb.xcb_get_property.argtypes = [
    POINTER(xcb_connection_t),
    uint8_t,
    xcb_window_t,
    xcb_atom_t,
    xcb_atom_t,
    uint32_t,
    uint32_t
]
xcb.xcb_get_property.restype = xcb_get_property_cookie_t

xcb.xcb_get_property_reply.argtypes = [
    POINTER(xcb_connection_t),
    xcb_get_property_cookie_t,
    POINTER(POINTER(xcb_generic_error_t))
]
xcb.xcb_get_property_reply.restype = POINTER(xcb_get_property_reply_t)

xcb.xcb_get_property_value_length.argtypes = [
    POINTER(xcb_get_property_reply_t)
]
xcb.xcb_get_property_value_length.restype = c_int

xcb.xcb_query_tree.argtypes = [
    POINTER(xcb_connection_t),
    xcb_window_t,
]
xcb.xcb_query_tree.restype = xcb_query_tree_cookie_t

xcb.xcb_query_tree_reply.argtypes = [
    POINTER(xcb_connection_t),
    xcb_query_tree_cookie_t,
    POINTER(POINTER(xcb_generic_error_t))
]
xcb.xcb_query_tree_reply.restype = POINTER(xcb_query_tree_reply_t)

xcb.xcb_query_tree_children.argtypes = [POINTER(xcb_query_pointer_reply_t)]
xcb.xcb_query_tree_children.restype = POINTER(xcb_window_t)

DEFAULT_SCREEN_NUMBER = ScreenNumber()
CONNECTION = xcb.xcb_connect(None, byref(DEFAULT_SCREEN_NUMBER))
DEFAULT_SCREEN = screen_of_display(CONNECTION, DEFAULT_SCREEN_NUMBER)
ROOT_WINDOW = DEFAULT_SCREEN.contents.root
# COOKIE = xcb.xcb_query_pointer(CONNECTION, ROOT_WINDOW)
ERROR_LIST = None
# REPLY = xcb.xcb_query_pointer_reply(CONNECTION, COOKIE, ERROR_LIST)
# print(REPLY.contents.response_type)
# COOKIE = xcb.xcb_get_property(
#     CONNECTION,
#     0,
#     ROOT_WINDOW,
#     XCB_ATOM_WM_CLASS,
#     XCB_ATOM_STRING,
#     0,
#     1
# )
# REPLY = xcb.xcb_get_property_reply(CONNECTION, COOKIE, ERROR_LIST)
# print(xcb.xcb_get_property_value_length(REPLY))
TREE_COOKIE = xcb.xcb_query_tree(CONNECTION, ROOT_WINDOW)
TREE_REPLY = xcb.xcb_query_tree_reply(CONNECTION, TREE_COOKIE, ERROR_LIST)
print(TREE_REPLY.contents.length)
