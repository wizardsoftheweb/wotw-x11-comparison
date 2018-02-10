# pylint: disable=missing-docstring,unused-argument,invalid-name,no-self-use
from __future__ import print_function

from unittest import TestCase

# from mock import call, MagicMock, patch
from mock import patch

from wotw_x11_comparison.common import WritesResults


class WritesResultsTestCase(TestCase):
    CSV_PATH = 'path/to/file'
    FIELDS = ['one', 'two']
    ENTRY = {'one': 'qqq', 'two': 47}

    def setUp(self):
        self.construct_result_writer()

    def wipe_result_writer(self):
        del self.result_writer

    def construct_result_writer(self):
        create_or_load_csv_patcher = patch.object(
            WritesResults,
            'create_or_load_csv'
        )
        self.mock_create_or_load_csv = create_or_load_csv_patcher.start()
        self.result_writer = WritesResults()
        self.mock_create_or_load_csv.stop()
        self.addCleanup(self.wipe_result_writer)
        # self.addCleanup(create_or_load_csv_patcher.stop)


class ConstructorUnitTests(WritesResultsTestCase):

    def setUp(self):
        create_or_load_csv_patcher = patch.object(
            WritesResults,
            'create_or_load_csv'
        )
        self.mock_create_or_load_csv = create_or_load_csv_patcher.start()
        self.addCleanup(create_or_load_csv_patcher.stop)
        self.result_writer = WritesResults(self.CSV_PATH, self.FIELDS)

    def test_csv_path(self):
        self.assertNotEquals(self.result_writer.active_csv, self.CSV_PATH)

    def test_fields(self):
        self.assertNotEquals(self.result_writer.active_fields, self.FIELDS)

    def test_csv_creation(self):
        self.mock_create_or_load_csv.assert_called_once_with(
            self.CSV_PATH,
            self.FIELDS
        )
