"""This file provides PointerWindowComparison"""

from xcffib import connect

from wotw_x11_comparison.common import RunsComparisons

from wotw_x11_comparison.pointer_window import XcbPointerWindow, XlibPointerWindow


class PointerWindowComparison(RunsComparisons):
    """
    This class compares the speed at which XCB and Xlib can find the window
    beneath the pointer
    """
    RUN_COUNT = 1000
    LIBRARIES = [XcbPointerWindow, XlibPointerWindow]
    FIELDS = [
        'library',
        # 'time',
        'root_x',
        'root_y',
        'window',
        'win_x',
        'win_y',
        'start',
        'gather_basics',
        'root_window',
        'recursion',
        'get_names',
        'parse_names',
        'exit'
    ]

    def run_single_trial_one_library(self, library):
        """Runs a single trial with one library"""
        connection = connect()
        setup = connection.get_setup()
        root_window = setup.roots[0].root
        window = self.warp_to_random_window(connection, root_window)
        position = self.get_pointer_position(connection, window)
        connection.disconnect()
        pointer_window = library()
        lib = pointer_window.library
        timing = pointer_window.find_window()[2]
        del pointer_window
        self.write_result_row({
            'library': lib,
            'root_x': position.root_x,
            'root_y': position.root_y,
            'window': window,
            'win_x': position.win_x,
            'win_y': position.win_y,
            'start': timing[0],
            'gather_basics': timing[1],
            'root_window': timing[2],
            'recursion': timing[3],
            'get_names': timing[4],
            'parse_names': timing[5],
            'exit': timing[6]
        })

    def run_single_trial_all_libraries(self):
        """Runs a single trial with all libraries"""
        for library in self.LIBRARIES:
            self.run_single_trial_one_library(library)

    def run_many_trials(self, count=None):
        """Runs many trials with all libraries"""
        if count is None:
            count = self.RUN_COUNT
        for _ in range(0, count):
            self.run_single_trial_all_libraries()
