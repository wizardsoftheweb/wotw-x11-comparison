# pylint: disable=W,C,R
from wotw_x11_comparison.common import HasLogger


class BasePointerWindow(HasLogger):

    def __init__(self, *args, **kwargs):
        super(BasePointerWindow, self).__init__(*args, **kwargs)
