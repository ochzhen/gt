import os
import configparser
import zlib
import hashlib
import gitobj
from common import ensure_empty_dir, ensure_dir, compute_sha1


class GitRepository:
    def __init__(self, path, is_new=False):
        self.worktree = path
        self.gitdir = os.path.join(path, '.git')
        self.config = configparser.ConfigParser()
        if is_new:
            self._init_new()
        else:
            self._init_existing()

    def _init_new(self):
        ensure_empty_dir(self.worktree)
        self._setup_git_directory()
        with open(self.path_in_gitdir('discription'), 'w') as f:
            f.write('Unnamed repository')
        with open(self.path_in_gitdir('HEAD'), 'w') as f:
            f.write(f'ref: refs/heads/master{os.linesep}')
        with open(self.path_in_gitdir('config'), 'w') as f:
            config = create_default_repo_config()
            config.write(f)

    def _setup_git_directory(self):
        ensure_dir(self.path_in_gitdir('branches'))
        ensure_dir(self.path_in_gitdir('objects'))
        ensure_dir(self.path_in_gitdir('refs', 'tags'))
        ensure_dir(self.path_in_gitdir('refs', 'heads'))

    def _init_existing(self):
        if not os.path.isdir(self.gitdir):
            raise Exception(f'Not a Git repository {self.worktree}')

        config_file = self.path_in_gitdir('config')
        if config_file and os.path.exists(config_file):
            self.config.read([config_file])
        else:
            raise Exception('Missing configuration file')

        version = int(self.config.get('core', 'repositoryformatversion'))
        if version != 0:
            raise Exception(f'repositoryformatversion {version} has different value from 0')
    
    def path_in_gitdir(self, *paths):
        '''Compute path relative to gitdir'''
        return os.path.join(self.gitdir, *paths)
    
    def read_object(self, sha: str) -> gitobj.GitObject:
        dirname, filename = parse_sha(sha)
        path = self.path_in_gitdir('objects', dirname, filename)
        if not os.path.exists(path):
            raise Exception(f'Object {sha} not found')

        with open(path, 'rb') as f:
            raw = zlib.decompress(f.read())

            space_idx = raw.find(b' ')
            type_name = raw[:space_idx].decode('ascii')

            null_idx = raw.find(b'\x00', space_idx)
            size = int(raw[space_idx + 1:null_idx].decode('ascii'))
            if size != len(raw) - null_idx - 1:
                raise Exception(f'Invalid object {sha}: inconsistent length')

            if type_name not in gitobj.git_object_types:
                raise Exception(f'Unknown type {type_name} for object {sha}')
            
            obj_type = gitobj.git_object_types[type_name]
            content_idx = null_idx + 1
            return obj_type(raw[content_idx:])
    
    def write_object(self, obj: gitobj.GitObject):
        content = obj.bcontent()
        sha = compute_sha1(content)
        
        dirname, filename = parse_sha(sha)
        dirpath = self.path_in_gitdir('objects', dirname)
        ensure_dir(dirpath)
        path = os.path.join(dirpath, filename)
        
        with open(path, 'wb') as f:
            f.write(zlib.compress(content))
        
        return sha


def create_default_repo_config():
    parser = configparser.ConfigParser()
    parser.add_section('core')
    parser.set('core', 'repositoryformatversion', '0')
    parser.set('core', 'filemode', 'false')
    parser.set('core', 'bare', 'false')
    return parser


def get_current_repo(path='.'):
    path = os.path.realpath(path)
    if os.path.isdir(os.path.join(path, '.git')):
        return GitRepository(path)
    
    parent = os.path.realpath(os.path.join(path, '..'))
    if parent == path:
        raise Exception('Not a git repository')
    return get_current_repo(parent)


def parse_sha(sha):
    return sha[:2], sha[2:]
