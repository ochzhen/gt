import os
import configparser
from common import ensure_empty_dir, ensure_dir


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

def create_default_repo_config():
    parser = configparser.ConfigParser()
    parser.add_section('core')
    parser.set('core', 'repositoryformatversion', '0')
    parser.set('core', 'filemode', 'false')
    parser.set('core', 'bare', 'false')
    return parser
