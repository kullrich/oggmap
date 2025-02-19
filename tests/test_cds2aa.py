#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
from oggmap import cds2aa


def test_define_parser():
    parse = cds2aa.define_parser()
    assert isinstance(parse, argparse.ArgumentParser)