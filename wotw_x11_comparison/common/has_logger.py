# pylint: disable=W,C,R
from logging import addLevelName, Formatter, getLogger, INFO, StreamHandler
from sys import stderr

SILLY = 5
addLevelName(SILLY, 'SILLY')
CONSOLE_HANDLER = StreamHandler(stream=stderr)
CONSOLE_FORMATTER = Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)


class HasLogger(object):

    def __init__(
            self,
            logger_name='wotw-x11-comparison',
            logger_level=INFO
    ):
        self.logger = getLogger(logger_name)
        self.logger.addHandler(CONSOLE_HANDLER)
        self.logger.silly = (
            lambda message, *args, **kwargs:
            self.logger.log(SILLY, message, *args, **kwargs)
        )
        self.logger.setLevel(logger_level)
