"""Assorted utility functions."""
# ==============================================================================
#  FILE: util.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  Last Modified: 2017-12-19
# ==============================================================================

import os
import subprocess


def find_root(path):
    """Return the root directory for a git repo given a path inside said repo.

    Notes
    -----
    Taken from [neoclide/denite-git](https://github.com/neoclide/denite-git/blob/master/rplugin/python3/denite/source/gitbranch.py)

    """
    while True:
        if path == '/' or os.path.ismount(path):
            return None
        p = os.path.join(path, '.git')
        if os.path.isdir(p):
            return path
        path = os.path.dirname(path)


def get_length(array):
    """Get the max string length for an attribute in a list."""
    max_count = int(0)
    for item in array:
        cur_len = len(item)
        if cur_len > max_count:
            max_count = cur_len
    return max_count


def get_width(array, attribute):
    """Get the max string length for an attribute in a collection."""
    max_count = int(0)
    for item in array:
        cur_attr = item[attribute]
        cur_len = len(cur_attr)
        if cur_len > max_count:
            max_count = cur_len
    return max_count


def git_do(location, command):
    """Run git commands from Python scripts.

    Arguments
    ---------
    location : str
        The target directory

    Returns
    -------
    list     : The utf-8 decoded search results

    """
    # cmd = f"git -C {location} {command}"
    cmd = f"git -C {location} status -s"
    try:
        p = subprocess.run(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)
    except subprocess.CalledProcessError:
        return []
    return p.stdout.decode('utf-8').split('\n')
