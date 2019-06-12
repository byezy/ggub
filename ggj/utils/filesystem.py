from os.path import join
from os import makedirs, fspath, getcwd
from pathlib import Path


def is_directory(target):
    return Path(target).is_dir()


def create_directory(name, parent = getcwd()):
    f = join(parent, name)
    makedirs(f)
    return f


def list_files(parent = getcwd(), exclude_dirs=True, recurse=True):
    p = Path(parent)
    return [fspath(x) for x in p.rglob("*", recursive=recurse) if not (x.is_dir() and exclude_dirs)]


def list_directories(parent = getcwd(), recurse=True):
    p = Path(parent)
    return [fspath(x) for x in p.rglob("*", recursive=recurse) if x.is_dir()]

