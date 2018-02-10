# pylint: disable=W,C,R

from xcb import connect

from wotw_x11_comparison.common import RunsComparisons

from wotw_x11_comparison.pointer_window import XcbPointerWindow, XlibPointerWindow


class PointerWindowComparison(RunsComparisons):
    RUN_COUNT = 1000
    LIBRARIES = [XcbPointerWindow, XlibPointerWindow]
    FIELDS = [
        'library',
        'time',
        'root_x',
        'root_y',
        'window',
        'win_x',
        'win_y'
    ]

    def __init__(self, *args, **kwargs):
        super(PointerWindowComparison, self).__init__(*args, **kwargs)

    def run_single_trial_one_library(self, pointer_window):
        # self.logger.info('Gathering X connection')
        connection = connect()
        # self.logger.debug("Connection: %s", connection)
        setup = connection.get_setup()
        # self.logger.debug("Setup: %s", setup)
        root_window = setup.roots[0].root
        # self.logger.debug("Root window: %s", root_window)
        window = self.warp_to_random_window(connection, root_window)
        # wm_name = self.get_window_property(connection, window, Atom.WM_NAME)
        position = self.get_pointer_position(connection, window)
        run_time = self.benchmark(pointer_window.find_window)
        self.write_result_row({
            'library': pointer_window.library,
            'time': run_time,
            'root_x': position.root_x,
            'root_y': position.root_y,
            'window': window,
            'win_x': position.win_x,
            'win_y': position.win_y,
        })

    def run_single_trial_all_libraries(self):
        for library in self.LIBRARIES:
            pointer_window = library()
            self.run_single_trial_one_library(pointer_window)

    def run_many_trials(self, count=None):
        if count is None:
            count = self.RUN_COUNT
        for _ in range(0, count):
            self.run_single_trial_all_libraries()
