import os
import re
import shutil
from functools import reduce
from pathlib import Path
import filecmp


class Sync:
    def __init__(self, src: Path, dst: Path):
        self._src = src
        self._dst = dst
        self._exclude_folders: list[str] = []
        self._exclude_files: list[str] = []
        self._exists_files: list[Path] = []
        self._exists_folders: list[Path]  = []


    def exclude(self, ftype: str, names: list[str]):
        if ftype == "folder":
            self._exclude_folders.extend(names)
        if ftype == "file":
            self._exclude_files.extend(names)


    def match(self, target: str , candidate: str):
        """Check if the candidate matches the target pattern."""
        if target == candidate: return True
        elif target.startswith("*."):
        # elif re.compile(r'^.*\.[a-zA-Z]+$').match(target):
        # elif re.compile(r"^.*\.*$").match(target):
            if target.split(".")[-1] == candidate.split(".")[-1]: return True
        return False

    def equal(self, target: Path , candidate: Path):
        if os.path.getsize(target) != os.path.getsize(candidate):
            return False
            # 再逐字节比较
        return filecmp.cmp(target, candidate, shallow=False)
        # with open(target, 'rb') as f1, open(candidate, 'rb') as f2:
        #     return f1.read() == f2.read()

    def is_new(self, candidate: Path):
        return not candidate.exists()

    def remove(self):
        for root, dirs, files in os.walk(self._dst):
            for file in files:
                _is_exists = False
                _target = Path(root).joinpath(file)
                for efi in self._exists_files:
                    if efi == _target: _is_exists = True
                if not _is_exists:
                    os.remove(_target)
        self.remove_empty_folder()

    def remove_empty_folder(self):
        for root, dirs, files in os.walk(self._dst, topdown=False):
            if self.is_folder_empty(root):
                shutil.rmtree(root)
                # os.remove(root)


    def is_folder_empty(self,folder_path):
        return not any(Path(folder_path).iterdir())


    def execute(self):
        base_depth = len(self._src.parts)
        for root, dirs, files in os.walk(self._src):
            current_depth = len(Path(root).parts) - base_depth
            for ex_folder in self._exclude_folders:
                if ex_folder in dirs:
                    dirs.remove(ex_folder)
            if current_depth != 0: self._exists_folders.append(Path(self._dst).joinpath(Path(root).name))
            for file in files:
                _is_exclude = False

                for ex_file in self._exclude_files:
                    if self.match(ex_file, file):
                        _is_exclude = True
                        break

                if not _is_exclude:
                    if current_depth == 0:
                        _candidate = Path(self._dst).joinpath(file)
                        if not Path(self._dst).exists():
                            Path(self._dst).mkdir(parents=True)
                        self._exists_files.append(_candidate)
                        if self.is_new(_candidate) or not self.equal(Path(root).joinpath(file), _candidate):
                            shutil.copy(Path(root).joinpath(file), _candidate)
                    else:
                        _folders: list = root.replace(str(self._src), "").split("\\")[1:]
                        _path = reduce(lambda x, y: x.joinpath(y), [*[Path(self._dst)], *_folders])
                        _candidate = _path.joinpath(file)
                        if not _path.exists():
                            _path.mkdir(parents=True)
                        self._exists_files.append(_candidate)
                        if  self.is_new(_candidate) or not self.equal(Path(root).joinpath(file), _candidate):
                            shutil.copy(Path(root).joinpath(file), _candidate)
        self.remove()


def sync_backend():
    sync = Sync(src=Path("D:\\repository\\github\\et\\et"),
                dst=Path("D:\\repository\\aws\\eclinical40_auto_ctms\\eclinicalEt\\backend\\et"))

    sync.exclude("folder", [".idea", ".venv", "data","__pycache__"])
    # sync.exclude("folder", [".idea", ".venv", "data"])
    sync.exclude("file",
                 ["*.log", "*.bak", "Thumbs.db", "desktop.ini", "sync.bat", "alembic.ini", "alchemy.db", ".env.local",
                  ".env.production", ".gitignore", "db.sqlite3", "sync.py","et_scaffold.py",".env.example"])
    sync.execute()

def sync_frontend():
    sync = Sync(src=Path("D:\\repository\\github\\et\\etui\\etui"),
                dst=Path("D:\\repository\\aws\\eclinical40_auto_ctms\\eclinicalEt\\frontend"))

    sync.exclude("folder", [".vscode" "node_modules"])
    sync.exclude("file",
                 ["*.log", "*.bak", "Thumbs.db", "desktop.ini", "sync.bat", "alembic.ini", "alchemy.db", ".env.local",
                  ".env.production","sync.bat"])
    sync.execute()

if __name__ == '__main__':
    sync_backend()
    # sync_frontend()
