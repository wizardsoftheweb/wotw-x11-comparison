"""This file provides WritesResults"""
# pylint: disable=unused-argument,invalid-name,too-few-public-methods
# pylint: disable=no-self-use,protected-access,unused-import,too-many-arguments

from csv import DictWriter, QUOTE_NONNUMERIC
from os.path import isfile

from sys import exit as sys_exit


class WritesResults(object):
    """This class collects result logging tools"""
    RESULTS_PATH = 'results.csv'
    FIELDS = []

    def __init__(self, csv_path=None, fields=None):
        self.active_csv = self.RESULTS_PATH
        self.active_fields = self.FIELDS
        self.create_or_load_csv(csv_path, fields)

    def create_or_load_csv(self, csv_path=None, fields=None):
        """Ensures the desired CSV exists and is ready for results"""
        if csv_path is None:
            csv_path = self.RESULTS_PATH
        self.active_csv = csv_path
        if fields is None:
            fields = self.FIELDS
        self.active_fields = fields
        if not isfile(self.active_csv):
            with open(self.active_csv, 'w+') as results_csv:
                writer = DictWriter(
                    results_csv,
                    fieldnames=self.active_fields,
                    quoting=QUOTE_NONNUMERIC
                )
                writer.writeheader()

    def write_result_row(self, entries_dict):
        """Writes a row of results to the spreadsheet"""
        with open(self.active_csv, 'a+') as results_csv:
            writer = DictWriter(
                results_csv,
                fieldnames=self.active_fields,
                quoting=QUOTE_NONNUMERIC
            )
            writer.writerow(entries_dict)
