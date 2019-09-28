import os
import re
import sys
import collections
import argparse
import hashlib
import zlib
import gitrepo
import gitobj
from common import compute_sha1


def main():
    argparser = create_argparser()
    args = argparser.parse_args(sys.argv[1:])
    if   args.command == 'add'          : cmd_add(args)
    elif args.command == 'cat-file'     : cmd_cat_file(args)
    elif args.command == 'checkout'     : cmd_checkout(args)
    elif args.command == 'commit'       : cmd_commit(args)
    elif args.command == 'hash-object'  : cmd_hash_object(args)
    elif args.command == 'init'         : cmd_init(args)
    elif args.command == 'log'          : cmd_log(args)
    elif args.command == 'ls-tree'      : cmd_ls_tree(args)
    elif args.command == 'merge'        : cmd_merge(args)
    elif args.command == 'rebase'       : cmd_rebase(args)
    elif args.command == 'rev-parse'    : cmd_rev_parse(args)
    elif args.command == 'rm'           : cmd_rm(args)
    elif args.command == 'show-ref'     : cmd_show_ref(args)
    elif args.command == 'tag'          : cmd_tag(args)

def create_argparser():
    parser = argparse.ArgumentParser(description='Execute git command')

    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True

    initsp = subparsers.add_parser('init', help='Initialize new repository')
    initsp.add_argument('path', metavar='directory', nargs='?', default='.', help='Location where to create the repository')

    catfilesp = subparsers.add_parser('cat-file', help='View content of repository object')
    catfilesp.add_argument('type', metavar='type', choices=['blob', 'commit', 'tag', 'tree'], help='Specify type')
    catfilesp.add_argument('object', metavar='object', help='The object to display')

    hashobjsp = subparsers.add_parser('hash-object', help='Compute object hash and optionally create a blob from file')
    hashobjsp.add_argument('-t', metavar='type', dest='type', choices=['blob', 'commit', 'tag', 'tree'], default='blob', help='Specify type')
    hashobjsp.add_argument('-w', dest='dry_run', action='store_false', help='Write the object to the database')
    hashobjsp.add_argument('path', help='Read object from <file>')

    return parser


def cmd_init(args):
    gitrepo.GitRepository(args.path)


def cmd_cat_file(args):
    repo = gitrepo.get_current_repo()
    obj = repo.read_object()
    sys.stdout.buffer.write(obj.serialize())


def cmd_hash_object(args):
    with open(args.path, 'rb') as f:
        obj = create_object(f.read(), args.type)
    
    if args.dry_run:
        sha = compute_sha1(obj.bcontent())
    else:
        repo = gitrepo.get_current_repo()
        sha = repo.write_object(obj)

    print(sha)


def create_object(data: bytes, type_name: str) -> gitobj.GitObject:
    if type_name not in gitobj.git_object_types:
        raise Exception(f'Unknown object type {type_name}')
    obj_type = gitobj.git_object_types[type_name]
    return obj_type(data)
