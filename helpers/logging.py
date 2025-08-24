
from traceback import * 
from os import makedirs, path, rename
from helpers.utils import BOLD, WHITE, RESET

class FileSystem:
    def __init__(self, file="main.log"):
        self.file = file

    def save(self, content: str, mode: str = "a", encoding: str = "utf-8"):
        makedirs(path.dirname(self.file) or ".", exist_ok=True)

        if path.exists(self.file):
            size = path.getsize(self.file)
            if size > 5 * 1024 * 1024:
                rename(self.file, self.file + ".old")

        with open(self.file, mode, encoding=encoding) as f:
            f.write(content)
