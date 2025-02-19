#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import argparse
from unittest.mock import patch
from oggmap import ncbitax


def test_define_parser():
    parse = ncbitax.define_parser()
    assert isinstance(parse, argparse.ArgumentParser)


def test_update_ncbi():
    #path = os.path.expanduser('~/.etetoolkit/taxa.sqlite')
    path = os.path.expanduser('/tmp/taxadb.sqlite')
    path_exist = os.path.exists(path)
    if not path_exist:
        update_parser = ncbitax.define_parser()
        with patch("sys.argv", ["ncbitax"]):  # Prevent pytest from injecting arguments
            update_args = update_parser.parse_args([])
        update_args.outdir = os.path.expanduser('/tmp')
        update_args.dbname = os.path.expanduser('/tmp/taxadb.sqlite')
        update_args.force = True
        ncbitax.update_ncbi(update_args)
        assert os.path.exists(path)