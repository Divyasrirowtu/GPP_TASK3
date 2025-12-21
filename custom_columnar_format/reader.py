class CustomReader:
    def __init__(self):
        pass  # keep existing init if any

    def read_all(self, filename):
        rows = []
        with open(filename, 'r', encoding='utf-8') as f:
            header = f.readline().strip().split(',')
            for line in f:
                values = line.strip().split(',')
                row = dict(zip(header, values))
                rows.append(row)
        return rows
