#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a json log of a git repository.
"""

from __future__ import print_function
import json
import sys
from .parser import parse_commits

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.3'

# -------------------------------------------------------------------
# Main


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    parser.add_argument(
        '--since',
        default=None,
        help=('Show commits more recent than a specific date. If present, '
              'this argument is passed through to "git log" unchecked. ')
    )
    parser.add_argument(
        '--compare',
        default=None,
        help=('Compares two branches. eg. "master..develop" ')
    )
    args = parser.parse_args()
    if sys.version_info < (3, 0):
        print(git2json(run_git_log(args.git_dir, args.compare, args.since)))
    else:
        print(git2jsons(run_git_log(args.git_dir, args.compare, args.since)))

# -------------------------------------------------------------------
# Main API functions


def git2jsons(s):
    return json.dumps(list(parse_commits(s)), ensure_ascii=False)


def git2json(fil):
    return json.dumps(list(parse_commits(fil.read())), ensure_ascii=False)


# -------------------------------------------------------------------
# Functions for interfacing with git


def run_git_log(git_dir=None, git_compare=None, git_since=None):
    '''run_git_log([git_dir]) -> File

    Run `git log --numstat --pretty=raw` on the specified
    git repository and return its stdout as a pseudo-File.'''
    import subprocess

    if git_compare is None:
        git_compare = ''

    if git_dir:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            git_compare,                
            '--numstat',
            '--pretty=raw'
        ]
    else:
        command = [
            'git', 
            'log', 
            git_compare,
            '--numstat', 
            '--pretty=raw']
    if git_since is not None:
        command.append('--since=' + git_since)
    raw_git_log = subprocess.Popen(
        command,
        stdout=subprocess.PIPE
    )
    if sys.version_info < (3, 0):
        return raw_git_log.stdout
    else:
        return raw_git_log.stdout.read().decode('utf-8', 'ignore')
