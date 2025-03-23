import unittest
import os
import csv
from src.main.adapters.csv_adapter import CsvAdapter

class TestCsvAdapter(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_output.csv'
        self.adapter = CsvAdapter(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_writes_headers_to_csv(self):
        headers = ['header1', 'header2', 'header3']
        self.adapter.write(headers)

        with open(self.test_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.assertEqual(next(reader), headers)

    def test_writes_empty_headers_to_csv(self):
        headers = []
        self.adapter.write(headers)

        with open(self.test_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.assertEqual(next(reader), headers)

if __name__ == "__main__":
    unittest.main()