import collections
from abc import ABC, abstractmethod, abstractproperty


class GitObject(ABC):
    def __init__(self, data=None):
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

    def bcontent(self) -> bytes:
        data = self.serialize()
        content = self.btype + b' ' + str(len(data)).encode() + b'\x00' + data
        return content


class GitBlob(GitObject):
    @property
    def btype(self):
        return b'blob'

    def serialize(self):
        return self.blobdata
    
    def deserialize(self, data):
        self.blobdata = data


class GitCommit(GitObject):
    @property
    def btype(self):
        return b'commit'
    
    def serialize(self):
        buffer = []
        for key in self.data.keys():
            if key == b'':
                continue
            values = self.data[key]
            for val in values:
                buffer.extend((key, b' ', val.replace(b'\n', b'\n '), b'\n'))
        buffer.extend((b'\n', self.data[b'']))
        return b''.join(buffer)
    
    def deserialize(self, data):
        ord_dict = collections.OrderedDict()
        
        def parse(self, data, start_idx):
            space_idx = data.find(b' ', start_idx)
            newline_idx = data.find(b'\n', start_idx)

            if space_idx < 0 or newline_idx < space_idx:
                assert(newline_idx == start_idx)
                ord_dict[b''] = data[start_idx+1:]
                return
            
            key = data[start_idx:space_idx]
            end_idx = data.find(b'\n', start_idx + 1)
            while data[end_idx + 1] == ord(' '):
                end_idx = data.find(b'\n', end_idx + 1)
            value = data[space_idx + 1: end_idx].replace(b'\n ', b'\n')

            if key in ord_dict:
                ord_dict[key].append(value)
            else:
                ord_dict[key] = [value]
            
            return self._parse(data, end_idx + 1)
        
        parse(data, 0)
        self.data = ord_dict
    
    def tree_sha(self):
        trees = self.data[b'tree']
        return trees[0].decode('ascii')


class GitTag(GitObject):
    pass


class GitTree(GitObject):
    @property
    def btype(self):
        return b'tree'

    def serialize(self) -> bytes:
        buffer = []
        for item in self.items:
            sha_num = int(item.sha, 16)
            sha_bytes = sha_num.to_bytes(20, byteorder='big')
            buffer.extend((item.mode, b' ', item.path, b'\x00', sha_bytes))
        return b''.join(buffer)
    
    def deserialize(self, data):
        self.items = []
        idx = 0
        while idx < len(data):
            space_idx = data.find(b' ', idx)
            mode = data[idx:space_idx]
            null_idx = data.find(b'\x00', space_idx)
            path = data[space_idx + 1:null_idx]
            sha_num = int.from_bytes(data[null_idx + 1:null_idx + 21], 'big')
            sha = hex(sha_num)[2:]
            self.items.append(GitTree.GitTreeItem(mode, path, sha))
            idx = null_idx + 21
    
    class GitTreeItem:
        def __init__(self, mode, path, sha):
            self.mode = mode
            self.path = path
            self.sha = sha


git_object_types = {
    'blob': GitBlob,
    'commit': GitCommit,
    'tag': GitTag,
    'tree': GitTree
}


def find_object_sha(repo, identifier):
    return identifier
