import os


def ensure_empty_dir(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f'{path} is not a directory')
        if len(os.listdir(path)) > 0:
            raise Exception(f'{path} directory is not empty')
    else:
        os.makedirs(path)


def ensure_dir(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f'Not a directory: {path}')
    else:
        os.makedirs(path)
