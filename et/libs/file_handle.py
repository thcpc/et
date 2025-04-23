import os
from pathlib import Path
import shutil


class FileHandle:
    @classmethod
    def block_no(cls):
        ...

    @classmethod
    def write_data(cls, file_path: Path, contents: str):
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, 'w') as f:
            f.write(contents)

    @classmethod
    def read_data(cls, file_path: Path):
        with open(file_path, 'r') as f:
            return f.read()

    @classmethod
    def move_data(cls, src: Path, dst: Path):
        shutil.move(src, dst)

    @classmethod
    def rm_data(cls, file_path: Path):
        if file_path.exists():
            os.remove(file_path)
