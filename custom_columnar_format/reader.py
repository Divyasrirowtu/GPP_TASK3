# reader.py
class CustomReader:
    def __init__(self):
        self.columns = []
        self.rows = []

    def read_all(self, file_path):
        """Read all rows from a CCF file into a list of dictionaries"""
        rows = []
        with open(file_path, 'r', encoding='utf-8') as f:
            headers = f.readline().strip().split(",")
            for line in f:
                values = line.strip().split(",")
                row = dict(zip(headers, values))
                rows.append(row)
        return rows
