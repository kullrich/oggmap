#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import argparse
import pandas as pd
from Bio.Phylo.Newick import Tree
from oggmap import qlin


def test_define_parser():
    parse = qlin.define_parser()
    assert isinstance(parse, argparse.ArgumentParser)


def test_get_qlin_q_argument():
    q = 'Danio rerio'
    info = qlin.get_qlin(q=q,
                         dbname=os.path.expanduser('/tmp/taxadb.sqlite'))
    assert isinstance(info, list)
    assert info[0] == q
    assert isinstance(info[3], dict)
    assert isinstance(info[-1], str)
    for info_index in [2, 4]:
        assert isinstance(info[info_index], list)
    assert isinstance(info[5], pd.DataFrame)


def test_get_qlin_qt_argument():
    qt = '7955'
    info = qlin.get_qlin(qt=qt,
                         dbname=os.path.expanduser('/tmp/taxadb.sqlite'))
    assert isinstance(info, list)
    assert info[1] == int(qt)
    assert isinstance(info[3], dict)
    assert isinstance(info[-1], str)
    for info_index in [2, 4]:
        assert isinstance(info[info_index], list)
    assert isinstance(info[5], pd.DataFrame)


def test_get_qlin_q_and_qt_argument():
    q = 'Danio rerio'
    qt = '7955'
    info = qlin.get_qlin(q=q,
                         qt=qt,
                         dbname=os.path.expanduser('/tmp/taxadb.sqlite'))
    assert isinstance(info, list)
    assert info[0] == q
    assert info[1] == int(qt)


def test_get_qlin_q_with_wrong_qt_argument():
    """If the name and taxid do not match then `oggmap` returns information
    based on the taxid."""
    q = 'Danio rerio'
    qt = '7956'
    info = qlin.get_qlin(q=q,
                         qt=qt,
                         dbname=os.path.expanduser('/tmp/taxadb.sqlite'))
    assert isinstance(info, list)
    assert info[0] != q
    assert info[1] == int(qt)


def test_lineage_topo():
    qt = '7955'
    tree = qlin.get_lineage_topo(qt=qt,
                                 dbname=os.path.expanduser('/tmp/taxadb.sqlite'))
    assert isinstance(tree, Tree)


def test_get_youngest_common():
    ql = ['A', 'B', 'C']
    tl = ['Q', 'N', 'A', 'C', 'B']
    assert qlin.get_youngest_common(ql, tl) == 'B'


def test_oldest_common():
    ql = ['A', 'B', 'C']
    tl = ['Q', 'N', 'A', 'C', 'B']
    assert qlin.get_oldest_common(ql, tl) == 'A'
