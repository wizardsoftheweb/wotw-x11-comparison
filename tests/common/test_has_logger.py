# pylint: disable=missing-docstring
# pylint: disable=no-self-use

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_x11_comparison.common import HasLogger


class ConstructorUnitTests(TestCase):

    @patch(
        'wotw_x11_comparison.common.has_logger.getLogger'
    )
    def test_logger_set(self, mock_get):
        mock_handler = MagicMock()
        mock_level = MagicMock()
        mock_logging = MagicMock()
        mock_logging.attach_mock(mock_handler, 'addHandler')
        mock_logging.attach_mock(mock_level, 'setLevel')
        mock_get.return_value = mock_logging
        HasLogger()
        mock_get.assert_has_calls([
            call(mock_get.mock_calls[0][1][0]),
            call().addHandler(mock_get.mock_calls[1][1][0]),
            call().setLevel(mock_get.mock_calls[2][1][0])
        ])
