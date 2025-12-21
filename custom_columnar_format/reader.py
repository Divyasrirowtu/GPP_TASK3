# reader.py
import csv

class CustomReader:
    def __init__(self):
        pass

    def read_all(self, file_path):
        """Minimal implementation to read CSV-like text for testing"""
        rows = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows

