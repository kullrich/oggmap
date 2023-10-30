#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import argparse
from oggmap import ncbitax


def test_define_parser():
    parse = ncbitax.define_parser()
    assert isinstance(parse, argparse.ArgumentParser)


def test_update_ncbi():
    path = os.path.expanduser('~/.etetoolkit/taxa.sqlite')
    path_exist = os.path.exists(path)
    if not path_exist:
        ncbitax.update_ncbi()
        assert os.path.exists(path)
