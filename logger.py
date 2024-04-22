import os

class Logger(object):
    def __init__(self, log_path, rewrite=False) -> None:
        self.log_path = log_path
        if os.path.exists(log_path) and not rewrite:
            os.remove(log_path)

    def verbose(self, file, message):
        with open(self.log_path, "a") as f:
            print(f"In {file}: {message}")
            f.write(f"In {file}: {message}\n")
