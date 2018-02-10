# pylint: disable=W,C,R
#!/usr/bin/env python
from __future__ import print_function

import csv
from os import path
import random
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

FIELDS = ['library', 'time', 'root_x', 'root_y', 'wm_name',  'win_x', 'win_y']
RESULTS_PATH = 'results.csv'
LIBRARY = 'XCB'


def get_property_value(reply):
    LOGGER.debug("Attempting to parse %s's value", reply)
    if isinstance(reply, GetPropertyReply):
        if 8 == reply.format:
            value = ''
            for chunk in reply.value:
                value += chr(chunk)
            LOGGER.silly("Parsed %s", value)
            return value
        elif reply.format in (16, 32):
            value = list(
                struct.unpack(
                    'I' * reply.value_len,
                    reply.value.buf()
                )
            )
            LOGGER.silly("Parsed %s", value)
            return value

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
    if first:
        if second:
            if first == second or len(first) > len(second):
                LOGGER.silly('Chose the first; same string or same length')
                return first
        LOGGER.silly('Chose the second; first is not equal and shorter')
        return second
    return ''


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


def get_unknown_atom(connection, atom, exists_only=False):
    cookie = connection.core.InternAtom(
        exists_only,
        len(atom),
        atom
    )
    reply = cookie.reply()
    setattr(Atom, atom, reply.atom)


def choose_a_random_window(connection, root_window):
    viable_windows = get_window_property(
        connection,
        root_window,
        getattr(Atom, '_NET_CLIENT_LIST')
    )
    window_index = random.randint(0, len(viable_windows) - 1)
    return viable_windows[window_index]


def move_to_random_position_in_window(connection, window):
    geometry = get_window_geometry(connection, window)
    connection.core.WarpPointer(
        Atom._None,
        window,
        0,
        0,
        0,
        0,
        random.randint(0, geometry.width),
        random.randint(0, geometry.height)
    )
    connection.flush()


def warp_to_random_window(connection, root_window):
    window = choose_a_random_window(connection, root_window)
    move_to_random_position_in_window(connection, window)
    return window


def create_or_load_csv():
    if not path.isfile(RESULTS_PATH):
        with open(RESULTS_PATH, 'w+') as results_csv:
            writer = csv.DictWriter(
                results_csv, fieldnames=FIELDS, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()


def write_result_row(time, position, wm_name):
    with open(RESULTS_PATH, 'a+') as results_csv:
        writer = csv.DictWriter(
            results_csv, fieldnames=FIELDS, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow({
            'library': LIBRARY,
            'time': time,
            'root_x': position.root_x,
            'root_y': position.root_y,
            'wm_name': wm_name,
            'win_x': position.win_x,
            'win_y': position.win_y,
        })


def run_single_trial():
    run_time = benchmark(find_window)
    connection, setup = gather_basics()
    root_window = get_root_window(setup)
    get_unknown_atom(connection, '_NET_CLIENT_LIST', True)
    window = warp_to_random_window(connection, root_window)
    window_name = get_window_property(connection, window, Atom.WM_NAME)
    position = connection.core.QueryPointer(root_window).reply()
    write_result_row(run_time, position, window_name)


def cli():
    create_or_load_csv()
    run_single_trial()
    # display_benchmark(find_window)
    # connection.core.WarpPointer(
    #     root_window,
    #     # root_window,
    #     Atom._None,
    #     0,
    #     0,
    #     geometry.width,
    #     geometry.height,
    #     random.randint(-geometry.width, geometry.width),
    #     random.randint(-geometry.height, geometry.height)
    # )
    # display_benchmark(find_window)
    sys_exit(0)

if '__main__' == __name__:
    cli()
