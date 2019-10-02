import os
import hashlib
import gitobj


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


def compute_sha1(content) -> str:
    return hashlib.sha1(content).hexdigest()


def is_blob(obj):
    return isinstance(obj, gitobj.GitBlob)


def is_commit(obj):
    return isinstance(obj, gitobj.GitCommit)


def is_tree(obj):
    return isinstance(obj, gitobj.GitTree)