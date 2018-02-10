# pylint: disable=missing-docstring,unused-argument,invalid-name,no-self-use
from __future__ import print_function

from os.path import join
from unittest import TestCase

# from mock import call, MagicMock, patch
from mock import MagicMock, patch

from wotw_x11_comparison.common import WritesResults


class WritesResultsTestCase(TestCase):
    CSV_PATH = join('path', 'to', 'file')
    FIELDS = ['one', 'two']
    ENTRY = {'one': 'qqq', 'two': 47}

    def setUp(self):
        self.construct_result_writer()

    def wipe_result_writer(self):
        del self.result_writer

    def construct_result_writer(self):
        open_patcher = patch(
            'wotw_x11_comparison.common.writes_results.open',
            return_value=MagicMock()
        )
        self.mock_open = open_patcher.start()
        self.addCleanup(open_patcher.stop)
        dict_writer_patcher = patch(
            'wotw_x11_comparison.common.writes_results.DictWriter',
            return_value=MagicMock()
        )
        self.mock_dict_writer = dict_writer_patcher.start()
        self.addCleanup(dict_writer_patcher.stop)
        create_or_load_csv_patcher = patch.object(
            WritesResults,
            'create_or_load_csv'
        )
        self.mock_create_or_load_csv = create_or_load_csv_patcher.start()
        self.result_writer = WritesResults()
        create_or_load_csv_patcher.stop()
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


class CreateOrLoadCsvUnitTests(WritesResultsTestCase):
    NONNUMERIC = 47

    @patch(
        'wotw_x11_comparison.common.writes_results.isfile',
        return_value=True
    )
    def test_defaults(self, mock_isfile):
        self.result_writer.create_or_load_csv()
        self.assertEquals(
            self.result_writer.active_csv,
            WritesResults.RESULTS_PATH
        )
        self.assertEquals(
            self.result_writer.active_fields,
            WritesResults.FIELDS
        )
        self.assertEquals(self.mock_open.call_count, 0)
        self.assertEquals(self.mock_dict_writer.call_count, 0)

    @patch(
        'wotw_x11_comparison.common.writes_results.QUOTE_NONNUMERIC',
        return_value=NONNUMERIC
    )
    @patch(
        'wotw_x11_comparison.common.writes_results.isfile',
        return_value=False
    )
    def test_creation(self, mock_isfile, mock_nonnumeric):
        self.mock_create_or_load_csv.stop()
        self.result_writer.create_or_load_csv(
            csv_path=self.CSV_PATH,
            fields=self.FIELDS
        )
        self.mock_dict_writer.assert_called_once_with(
            self.mock_dict_writer.mock_calls[0][1][0],
            fieldnames=self.FIELDS,
            quoting=mock_nonnumeric
        )
