class CustomReader:
    def read(self, file_path):
        with open(file_path, "rb") as f:
            return [line.decode().strip() for line in f]

