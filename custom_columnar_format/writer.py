class CustomWriter:
    def write(self, data, file_path):
        with open(file_path, "wb") as f:
            for value in data:
                f.write(str(value).encode() + b"\n")

