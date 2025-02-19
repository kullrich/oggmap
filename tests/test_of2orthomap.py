#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import pandas as pd
from oggmap import datasets, of2orthomap


ensembl113_last_oc, ensembl113_last_og, ensembl113_last_sl = datasets.ensembl113_last(datapath='/tmp')
dbname='/tmp/taxadb.sqlite'

def test_define_parser():
    parse = of2orthomap.define_parser()
    assert isinstance(parse, argparse.ArgumentParser)

def test_of2orthomap_continuity_false():
    query_orthomap, orthofinder_species_list, of_species_abundance = of2orthomap.get_orthomap(
        seqname='7955.danio_rerio.pep',
        qt='7955',
        oc=ensembl113_last_oc,
        og=ensembl113_last_og,
        sl=ensembl113_last_sl,
        continuity=False,
        quiet=True,
        dbname=dbname)
    assert isinstance(query_orthomap, pd.DataFrame)
    assert (query_orthomap.columns == ['seqID', 'Orthogroup', 'PSnum', 'PStaxID', 'PSname']).all()
    assert isinstance(orthofinder_species_list, pd.DataFrame)
    assert isinstance(of_species_abundance, pd.DataFrame)
    # Ask KU about the relationship of these three dataframes.
    # check the index in the `of_species_abundance`


def test_of2orthomap_continuity_true():
    query_orthomap, orthofinder_species_list, of_species_abundance = of2orthomap.get_orthomap(
        seqname='7955.danio_rerio.pep',
        qt='7955',
        oc=ensembl113_last_oc,
        og=ensembl113_last_og,
        sl=ensembl113_last_sl,
        continuity=True,
        quiet=True,
        dbname=dbname)
    assert isinstance(query_orthomap, pd.DataFrame)
    assert (query_orthomap.columns == ['seqID', 'Orthogroup', 'PSnum', 'PStaxID', 'PSname', 'PScontinuity']).all()
    assert isinstance(orthofinder_species_list, pd.DataFrame)
    assert isinstance(of_species_abundance, pd.DataFrame)
