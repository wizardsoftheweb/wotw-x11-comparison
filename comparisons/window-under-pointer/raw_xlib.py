# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import print_function

from ctypes import byref, CDLL, c_char_p, c_int, c_long, c_uint, c_ulong, POINTER, Structure
from logging import addLevelName, Formatter, getLogger, INFO, StreamHandler
from sys import exit as sys_exit, stderr
from time import time as time_now

SILLY = 5
addLevelName(SILLY, 'SILLY')
LOGGER = getLogger('wotw-macro')
CONSOLE_HANDLER = StreamHandler(stream=stderr)
CONSOLE_FORMATTER = Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.silly = (
    lambda message, *args, **kwargs:
    LOGGER.log(SILLY, message, *args, **kwargs)
)
LOGGER.setLevel(INFO)

# from pyglet.libs.x11 import xlib

xlib = CDLL('libX11.so.6')


class Display(Structure):
    # https://github.com/mirror/libX11/blob/libX11-1.6.5/include/X11/Xlib.h#L484
    # A Display should be treated as opaque by application code
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
    # https://tronche.com/gui/x/xlib/ICC/client-to-window-manager/converting-string-lists.html
    _fields_ = [
        ('value', c_char_p),
        ('encoding', IGNORED_FOR_NOW),
        ('format', c_int),
        ('nitems', c_ulong)
    ]


class XWindowAttributes(Structure):
    # https://tronche.com/gui/x/xlib/window-information/XGetWindowAttributes.html
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


def whoops(display, call, result):
    LOGGER.error("%s isn't truthy", result)
    LOGGER.critical("Something went wrong with %s", call)
    close_the_display(display)


def gather_basics(display_index=None):
    LOGGER.info('Gathering display and root window')
    LOGGER.debug("Display index: %s", display_index)
    display = xlib.XOpenDisplay(display_index)
    LOGGER.debug("Display: %s", display)
    screen = xlib.XDefaultScreen(display)
    LOGGER.debug("Screen: %s", screen)
    root_window = xlib.XRootWindow(display, screen)
    LOGGER.debug("Root Window: %s", root_window)
    return [display, root_window]


def get_mouse_windows(display, root_window):
    LOGGER.debug(
        "Determining mouse position relative to window %s",
        root_window
    )
    (root_reference, parent_reference) = (Window(), Window())
    (root_x, root_y) = (Coordinate(), Coordinate())
    (win_x, win_y) = (Coordinate(), Coordinate())
    mask = c_ulong()
    result = xlib.XQueryPointer(
        display,
        root_window,
        byref(root_reference),
        byref(parent_reference),
        byref(root_x),
        byref(root_y),
        byref(win_x),
        byref(win_y),
        byref(mask)
    )
    if not result:
        whoops(display, 'XQueryPointer', result)
    return [root_reference, parent_reference]


def get_window_under_pointer(display, window):
    LOGGER.silly(
        "Searching for the window under the pointer relative to window %s",
        window
    )
    root_window, child_window = get_mouse_windows(display, window)
    if 0 != child_window.value and root_window != child_window:
        return get_window_under_pointer(display, child_window)
    LOGGER.debug("No other viable children found; returning %s", window)
    return window


def get_window_names(display, window):
    LOGGER.debug("Naming window %s", window)
    name = c_char_p()
    xlib.XFetchName(display, window, byref(name))
    LOGGER.silly("WM Name: %s", name.value)
    props = XTextProperty()
    xlib.XGetWMIconName(display, window, byref(props))
    LOGGER.silly("WM Icon Name: %s", props.value)
    return [name.value, props.value]


def parse_names(first, second):
    LOGGER.debug("Comparing %s and %s", first, second)
    if first == second or len(first) > len(second):
        LOGGER.silly('Chose the first; same string or same length')
        return first
    LOGGER.silly('Chose the second; first is not equal and shorter')
    return second


def close_the_display(display):
    LOGGER.info("Closing the display")
    xlib.XCloseDisplay(display)


def find_window():
    LOGGER.info('Launching')
    display, root_window = gather_basics()
    LOGGER.info('Beginning search')
    window = get_window_under_pointer(display, root_window)
    LOGGER.info("Window candidate is %s", window)
    names = get_window_names(display, window)
    probable_window_name = parse_names(*names)
    LOGGER.info("Picked %s", probable_window_name)
    close_the_display(display)


def benchmark(method_to_benchmark, *args, **kwargs):
    start = time_now()
    method_to_benchmark(*args, **kwargs)
    end = time_now()
    return end - start


def display_benchmark(method_to_benchmark, *args, **kwargs):
    run_length = benchmark(method_to_benchmark, *args, **kwargs)
    milli_run_length = run_length * 1000
    LOGGER.info(
        """Wrapping up
        Runtime
        {: >14}: {: > 10.4f}
        {: >14}: {: > 10.4f}
        {: >14}: {: > 10.4f}
        {: >14}: {: > 5d}
        """.format(
            'seconds', run_length,
            'milliseconds', milli_run_length,
            'microseconds', milli_run_length * 1000,
            'Ops per second',
            int(1000 / milli_run_length)
        )
    )


def cli():
    display_benchmark(find_window)
    sys_exit(0)

if '__main__' == __name__:
    cli()
