"""
This file provides XlibPointerWindow as well as Xlib component dependencies
"""
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

from ctypes import byref, CDLL, c_char_p, c_int, c_long, c_uint, c_ulong, POINTER, Structure

from wotw_x11_comparison.pointer_window import BasePointerWindow

xlib = CDLL('libX11.so.6')


class Display(Structure):
    """
    A Display should be treated as opaque by application code
    @see https://github.com/mirror/libX11/blob/libX11-1.6.5/include/X11/Xlib.h#L484
    """
    _fields_ = [
        ('_opaque_struct', c_int)
    ]

Window = c_ulong
Coordinate = c_int

# https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
# int map_state;          /* IsUnmapped, IsUnviewable, IsViewable */
IsUnmapped = 0
IsUnviewable = 1
IsViewable = 2

IGNORED_FOR_NOW = POINTER(c_int)


class XTextProperty(Structure):
    """
    Holds text information
    @see https://tronche.com/gui/x/xlib/ICC/client-to-window-manager/converting-string-lists.html
    """
    _fields_ = [
        ('value', c_char_p),
        ('encoding', IGNORED_FOR_NOW),
        ('format', c_int),
        ('nitems', c_ulong)
    ]


class XWindowAttributes(Structure):
    """
    Holds window attributes
    @see https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
    """
    _fields_ = [
        ('x', Coordinate),
        ('y', Coordinate),
        ('width', c_uint),
        ('height', c_uint),
        ('border_width', c_uint),
        ('depth', c_uint),
        ('visual', IGNORED_FOR_NOW),
        ('root', Window),
        ('class', c_int),
        ('bit_gravity', c_int),
        ('win_gravity', c_int),
        ('backing_store', c_int),
        ('backing_planes', c_ulong),
        ('backing_pixel', c_ulong),
        ('save_under', c_int),
        ('colormap', IGNORED_FOR_NOW),
        ('map_installed', c_int),
        ('map_state', c_int),
        ('all_event_masks', c_long),
        ('your_event_mask', c_long),
        ('do_not_propagate_mask', c_long),
        ('override_redirect', c_int),
        ('screen', IGNORED_FOR_NOW),
    ]

xlib.XOpenDisplay.argtypes = [c_char_p]
xlib.XOpenDisplay.restype = POINTER(Display)
xlib.XDefaultScreen.argtypes = [POINTER(Display)]
xlib.XDefaultScreen.restype = c_int
xlib.XRootWindow.argtypes = [POINTER(Display), c_int]
xlib.XRootWindow.restype = Window
xlib.XQueryPointer.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Window),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(c_ulong)
]
xlib.XQueryPointer.restype = c_int
xlib.XQueryTree.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Window),
    POINTER(POINTER(Window)),
    POINTER(c_uint)
]
xlib.XQueryTree.restype = c_int
xlib.XGetGeometry.argtypes = [
    POINTER(Display),
    Window,
    POINTER(Window),
    POINTER(Coordinate),
    POINTER(Coordinate),
    POINTER(c_uint),
    POINTER(c_uint),
    POINTER(c_uint),
    POINTER(c_uint)
]
xlib.XGetGeometry.restype = c_int
xlib.XGetWindowAttributes.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XWindowAttributes)
]
xlib.XGetWindowAttributes.restype = c_int
xlib.XCloseDisplay.argtypes = [POINTER(Display)]
xlib.XCloseDisplay.restype = c_int
xlib.XFetchName.argtypes = [POINTER(Display), Window, POINTER(c_char_p)]
xlib.XFetchName.restype = c_int
xlib.XGetWMIconName.argtypes = [
    POINTER(Display),
    Window,
    POINTER(XTextProperty)
]
xlib.XGetWMIconName.restype = c_int


class XlibPointerWindow(BasePointerWindow):
    """
    This class uses Xlib to determine the window beneath the pointer
    """

    library = 'xlib'

    def gather_basics(self):
        """Sets up the display and screen"""
        self.logger.info('Gathering display and root window')
        display = xlib.XOpenDisplay(None)
        self.logger.debug("Display: %s", display)
        screen = xlib.XDefaultScreen(display)
        self.logger.debug("Screen: %s", screen)
        return [display, screen]

    def get_root_window(self, lib_primary, lib_secondary):
        """Pulls the root window"""
        root_window = xlib.XRootWindow(lib_primary, lib_secondary)
        self.logger.debug("Root Window: %s", root_window)
        return root_window

    def get_mouse_windows(self, lib_primary, window):
        """Finds the children of window beneath the pointer (if any)"""
        self.logger.debug(
            "Determining mouse position relative to window %s",
            window
        )
        (root_reference, parent_reference) = (Window(), Window())
        (root_x, root_y) = (Coordinate(), Coordinate())
        (win_x, win_y) = (Coordinate(), Coordinate())
        mask = c_ulong()
        xlib.XQueryPointer(
            lib_primary,
            window,
            byref(root_reference),
            byref(parent_reference),
            byref(root_x),
            byref(root_y),
            byref(win_x),
            byref(win_y),
            byref(mask)
        )
        return [root_reference.value, parent_reference.value]

    def get_window_names(self, lib_primary, window):
        """Gets WM_NAME and WM_ICON_NAME for the specified window"""
        self.logger.debug("Naming window %s", window)
        name = c_char_p()
        xlib.XFetchName(lib_primary, window, byref(name))
        self.logger.silly("WM Name: %s", name.value)
        props = XTextProperty()
        xlib.XGetWMIconName(lib_primary, window, byref(props))
        self.logger.silly("WM Icon Name: %s", props.value)
        return [name.value, props.value]

    def gracefully_exit_x(self, lib_primary):
        """Gracefully disconnects from the X server"""
        xlib.XCloseDisplay(lib_primary)
