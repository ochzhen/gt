from abc import ABC, abstractmethod, abstractproperty

git_object_types = {
    'blob': GitBlob,
    'commit': GitCommit,
    'tag': GitTag,
    'tree': GitTree
}

class GitObject(ABC):
    def __init__(self, data=None):
        self.repo = repo
        if data is not None:
            self.deserialize(data)
    
    @abstractproperty
    def btype(self):
        pass
    
    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self, data):
        pass


class GitBlob(GitObject):
    @property
    def btype(self):
        return b'blob'

    def serialize(self):
        return self.blobdata
    
    def deserialize(self, data):
        self.blobdata = data


class GitCommit(GitObject):
    pass


class GitTag(GitObject):
    pass


class GitTree(GitObject):
    pass
