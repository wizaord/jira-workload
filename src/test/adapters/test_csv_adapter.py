"""
Test cases for the CsvAdapter class.
"""
import csv
import os
import unittest

from src.main.adapters.csv_adapter import CsvAdapter


class TestCsvAdapter(unittest.TestCase):
    """Test cases for the CsvAdapter class"""

    def setUp(self):
        """Set up the test case"""
        self.test_file = 'test_output.csv'
        self.adapter = CsvAdapter(self.test_file)

    def tearDown(self):
        """Tear down the test case"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_writes_headers_to_csv(self):
        """Test that the adapter writes headers to the csv file"""
        headers = ['header1', 'header2', 'header3']
        self.adapter.write(headers, [])

        with open(self.test_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.assertEqual(next(reader), ['header1;header2;header3'])

    def test_writes_empty_headers_to_csv(self):
        """Test that the adapter writes empty headers to the csv file"""
        headers = []
        self.adapter.write(headers, [])

        with open(self.test_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            self.assertEqual(next(reader), headers)


if __name__ == "__main__":
    unittest.main()
