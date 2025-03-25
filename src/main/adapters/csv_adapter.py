"""
CsvAdapter class
"""
import csv
import logging

logger = logging.getLogger(__name__)

class CsvAdapter:
    """Class to write in a CSV file"""

    def __init__(self, file_path: str):
        """Constructor of the class"""
        self.file_path = file_path

    def write(self, headers: list[str], rows: list[dict]):
        """Write the headers in the file"""
        with open(self.file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=";")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
