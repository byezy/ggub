from os.path import join
from os import makedirs, fspath
from pathlib import Path


def create_directory(parent, name):
    f = join(parent, name)
    makedirs(f)
    return f


def list_files(directory, exclude_dirs=True):
    p = Path(directory)
    f = [fspath(x) for x in p.rglob("*") if not (x.is_dir() and exclude_dirs)]
    return f
