#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import pathlib;
import sys;

from time import sleep as time_sleep;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODIFICATIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sleep(t: int):
    '''
    Sleeps t milliseconds.
    '''
    time_sleep(t/1000);
    return;

def create_path_if_not_exists(
    path: str,
    as_directory: bool = True,
) -> bool:
    '''
    Creates a path, if it does not already exist.
    '''
    if not as_directory:
        path = os.path.dirname(path);
    pathlib.Path(path).mkdir(
        parents=True,
        exist_ok=True,
    );
    return pathlib.Path(path).is_dir();

def create_file_if_not_exists(path: str) -> bool:
    '''
    Creates a file, if it does not already exist.
    '''
    if not create_path_if_not_exists(path=path, as_director=False):
        return False;
    pathlib.Path(path).touch(
        exist_ok=True,
    );
    return pathlib.Path(path).exists();

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'create_file_if_not_exists',
    'create_path_if_not_exists',
    'os',
    'pathlib',
    'sleep',
    'sys',
];
