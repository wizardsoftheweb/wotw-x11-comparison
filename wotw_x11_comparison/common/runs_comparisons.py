"""This file provides RunsComparisons"""

from time import time as time_now

from wotw_x11_comparison.common import MovesMouse, WritesResults


class RunsComparisons(WritesResults, MovesMouse):
    """This class combines everything necessary to run comparisons"""

    def __init__(self, *args, **kwargs):
        for base in RunsComparisons.__bases__:
            base.__init__(self, *args, **kwargs)

    @staticmethod
    def benchmark(action_to_benchmark, *args, **kwargs):
        """This method simply clocks start and end time"""
        start = time_now()
        action_to_benchmark(*args, **kwargs)
        end = time_now()
        return end - start
