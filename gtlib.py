import os
import re
import sys
import collections
import argparse
import hashlib
import zlib
import gitrepo


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


def cmd_init(args):
    gitrepo.GitRepository(args.path)


def cmd_cat_file(args):
    repo = gitrepo.get_current_repo()
    obj = repo.read_object()
    sys.stdout.buffer.write(obj.serialize())
