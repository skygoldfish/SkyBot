import os

def make_dir(path: str):
    if path == '.':
        return
    if not file_is_exist(path):
        os.mkdir(path)

def file_is_exist(path: str) -> bool:
    return os.path.exists(path)
