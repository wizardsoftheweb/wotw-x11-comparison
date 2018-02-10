# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

import struct
import xcb
from xcb.xproto import *
from xcb import Extension
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


def get_property_value(reply):
    LOGGER.debug("Attempting to parse %s's value", reply)
    if isinstance(reply, GetPropertyReply):
        if 8 == reply.format:
            value = ''
            for chunk in reply.value:
                value += chr(chunk)
            LOGGER.silly("Parsed %s", value)
            return value
        else:
            LOGGER.warning(
                "Unmanaged format %s; results may be wrong",
                reply.format
            )
    LOGGER.warning("The reply might not be valid: %s", reply)
    return None


def get_window_property(connection, window, atom):
    LOGGER.debug("Getting property %s from window %s", atom, window)
    cookie = connection.core.GetProperty(
        False,
        window,
        atom,
        GetPropertyType.Any,
        0,
        2 ** 32 - 1
    )
    reply = cookie.reply()
    return get_property_value(reply)


def gather_basics():
    LOGGER.info('Gathering X connection')
    connection = xcb.connect()
    LOGGER.debug("Connection: %s", connection)
    setup = connection.get_setup()
    LOGGER.debug("Setup: %s", setup)
    return [connection, setup]


def get_mouse_windows(connection, root_window):
    cookie = connection.core.QueryPointer(root_window)
    reply = cookie.reply()
    return [reply.root, reply.child]


def get_window_under_pointer(connection, window):
    LOGGER.silly(
        "Searching for the window under the pointer relative to window %s",
        window
    )
    root_window, child_window = get_mouse_windows(connection, window)
    if child_window != 0 and child_window != root_window:
        return get_window_under_pointer(connection, child_window)
    LOGGER.debug("No other viable children found; returning %s", window)
    return window


def get_window_names(connection, window):
    LOGGER.debug("Naming window %s", window)
    wm_name = get_window_property(connection, window, Atom.WM_NAME)
    LOGGER.silly("WM Name: %s", wm_name)
    wm_icon_name = get_window_property(connection, window, Atom.WM_ICON_NAME)
    LOGGER.silly("WM Icon Name: %s", wm_icon_name)
    return [wm_name, wm_icon_name]


def parse_names(first, second):
    LOGGER.debug("Comparing %s and %s", first, second)
    if first == second or len(first) > len(second):
        LOGGER.silly('Chose the first; same string or same length')
        return first
    LOGGER.silly('Chose the second; first is not equal and shorter')
    return second


def get_root_window(setup):
    LOGGER.debug('Discovering the root window')
    return setup.roots[0].root


def find_window():
    LOGGER.info('Launching')
    connection, setup = gather_basics()
    root_window = get_root_window(setup)
    LOGGER.info('Beginning search')
    window = get_window_under_pointer(connection, root_window)
    LOGGER.info("Window candidate is %s", window)
    names = get_window_names(connection, window)
    probable_window_name = parse_names(*names)
    LOGGER.info("Picked %s", probable_window_name)


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


def get_window_geometry(connection, window):
    cookie = connection.core.GetGeometry(window)
    return cookie.reply()


def cli():
    connection, setup = gather_basics()
    root_window = get_root_window(setup)
    geometry = get_window_geometry(connection, root_window)
    for key in dir(geometry):
        print(key)
    # display_benchmark(find_window)
    sys_exit(0)

if '__main__' == __name__:
    cli()
