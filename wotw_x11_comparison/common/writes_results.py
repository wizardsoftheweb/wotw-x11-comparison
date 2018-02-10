# pylint: disable=W,C,R

from csv import DictWriter, QUOTE_NONNUMERIC
from os.path import isfile

from sys import exit as sys_exit


class WritesResults(object):
    RESULTS_PATH = 'results.csv'
    FIELDS = []

    def __init__(self, csv_path=None, fields=None):
        self.active_csv = self.RESULTS_PATH
        self.active_fields = self.FIELDS
        self.create_or_load_csv(csv_path, fields)

    def create_or_load_csv(self, csv_path=None, fields=None):
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
        with open(self.active_csv, 'a+') as results_csv:
            writer = DictWriter(
                results_csv,
                fieldnames=self.active_fields,
                quoting=QUOTE_NONNUMERIC
            )
            writer.writerow(entries_dict)
