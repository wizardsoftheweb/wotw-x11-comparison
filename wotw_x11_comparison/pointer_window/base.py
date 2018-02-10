"""This file provides BasePointerWindow"""
# pylint: disable=unused-argument,invalid-name,too-few-public-methods
# pylint: disable=no-self-use,protected-access,unused-import,too-many-arguments

from abc import ABCMeta, abstractmethod

from wotw_x11_comparison.common import HasLogger


class BasePointerWindow(HasLogger):
    """
    This abstract class collects common components to detect the window
    underneath the pointer
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def gather_basics(self):
        """Sets up the primary and secondary sources"""

    @abstractmethod
    def get_root_window(self, lib_primary, lib_secondary):
        """Gets the root window"""

    @abstractmethod
    def get_mouse_windows(self, lib_primary, window):
        """Finds the children of window beneath the pointer (if any)"""

    def get_window_under_pointer(self, lib_primary, window):
        """
        Recursively checks windows and their children beneath the pointer,
        beginning with the root window
        """
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
        """Gets WM_NAME and WM_ICON_NAME for the specified window"""

    def parse_names(self, first, second):
        """Finds the longest name"""
        self.logger.debug("Comparing %s and %s", first, second)
        if first:
            if second:
                if len(first) < len(second):
                    self.logger.silly(
                        'Chose the second; same string or same length'
                    )
                    return second
            self.logger.silly(
                'Chose the first; second is equal or shorter'
            )
            return first
        elif second:
            return second
        return ''

    def find_window(self):
        """Attempts to find the window underneath the pointer"""
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
