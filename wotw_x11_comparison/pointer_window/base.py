# pylint: disable=W,C,R

from abc import ABCMeta, abstractmethod

from wotw_x11_comparison.common import HasLogger


class BasePointerWindow(HasLogger):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(BasePointerWindow, self).__init__(*args, **kwargs)

    @abstractmethod
    def gather_basics(self):
        """Placeholder"""

    @abstractmethod
    def get_root_window(self, lib_primary, lib_secondary):
        """Placeholder"""

    @abstractmethod
    def get_mouse_windows(self, lib_primary, window):
        """Placeholder"""

    def get_window_under_pointer(self, lib_primary, window):
        self.logger.silly(
            "Searching for the window under the pointer relative to window %s",
            window
        )
        root_window, child_window = self.get_mouse_windows(lib_primary, window)
        if child_window != 0 and child_window != root_window:
            return self.get_window_under_pointer(lib_primary, child_window)
        self.logger.debug(
            "No other viable children found; returning %s",
            window
        )
        return window

    @abstractmethod
    def get_window_names(self, lib_primary, window):
        """Placeholder"""

    def parse_names(self, first, second):
        self.logger.debug("Comparing %s and %s", first, second)
        if first:
            if second:
                if first == second or len(first) > len(second):
                    self.logger.silly(
                        'Chose the first; same string or same length'
                    )
                    return first
            self.logger.silly(
                'Chose the second; first is not equal and shorter'
            )
            return second
        return ''

    def find_window(self):
        self.logger.info('Launching')
        lib_primary, lib_secondary = self.gather_basics()
        root_window = self.get_root_window(lib_primary, lib_secondary)
        self.logger.info('Beginning search')
        window = self.get_window_under_pointer(lib_primary, root_window)
        self.logger.info("Window candidate is %s", window)
        names = self.get_window_names(lib_primary, window)
        probable_window_name = self.parse_names(*names)
        self.logger.info("Picked %s", probable_window_name)
        return [window, probable_window_name]
