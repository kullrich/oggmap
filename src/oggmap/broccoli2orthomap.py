#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
Author: Kristian K Ullrich
date: February 2025
email: ullrich@evolbio.mpg.de
License: GPL-3
"""

import os
import sys
import zipfile
import argparse
import pandas as pd
from oggmap import of2orthomap, qlin


def define_parser():
    """
    A helper function for using `broccoli2orthomap.py` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    broccoli2orthomap_example = '''broccoli2orthomap example:

    # download Broccoli example:
    $ wget https://zenodo.org/records/14935293/files/broccoli_example_table_OGs_protein_counts.txt
    $ wget https://zenodo.org/records/14935293/files/broccoli_example_table_OGs_protein_names.txt
    $ wget https://zenodo.org/records/14935293/files/broccoli_example_species_list.tsv

    # extract orthomap:
    $ broccoli2orthomap -seqname proteome.selected_transcript.ath.fasta -qt 3702 \\
      -sl broccoli_example_species_list.tsv \\
      -oc broccoli_example_table_OGs_protein_counts.txt \\
      -og broccoli_example_table_OGs_protein_names.txt \\
      -dbname taxadb.sqlite
    '''
    parser = argparse.ArgumentParser(
        prog='broccoli2orthomap',
        usage='%(prog)s [options] [<arguments>...]',
        description='extract orthomap from Broccoli output for query species',
        epilog=broccoli2orthomap_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_argparse_args(parser=parser)
    return parser


def add_argparse_args(parser: argparse.ArgumentParser):
    """
    This function attaches individual argument specifications to the parser.

    :param parser: An argparse.ArgumentParser.

    :type parser: argparse.ArgumentParser
    """
    parser.add_argument('-seqname',
                        help='sequence name of the query species in Broccoli '
                             '(see column names of  <table_OGs_protein_counts.txt>)')
    parser.add_argument('-qt',
                        help='query species taxID (e.g. use <oggmap qlin -h> to get taxID)')
    parser.add_argument('-sl',
                        help='species list as <Broccoli name><tab><species taxID> '
                             '(only samples in this list will be processed)')
    parser.add_argument('-oc',
                        help='specify Broccoli <table_OGs_protein_counts.txt> (see dir_step3 directory)')
    parser.add_argument('-og',
                        help='specify Broccoli <table_OGs_protein_names.txt> (see dir_step3 directory)')
    parser.add_argument('-out',
                        help='specify output file <orthomap.tsv> (default: orthomap.tsv)',
                        default='orthomap.tsv')
    parser.add_argument('-overwrite',
                        help='specify if existing output file should be overwritten (default: True)',
                        default=True,
                        type=bool)
    parser.add_argument('-dbname',
                        help='taxadb.sqlite file')


def get_broccoli_orthomap(seqname,
                          qt,
                          sl,
                          oc,
                          og,
                          out=None,
                          quiet=False,
                          continuity=True,
                          overwrite=True,
                          ncbi=None,
                          dbname=None):
    """
    This function return an orthomap for a given query species and Broccoli input data.

    :param qt: Query species taxID.
    :param sl: Path to species list file containing <Broccoli name><tab><species taxID>.
    :param oc: Path to Broccoli result <table_OGs_protein_counts.txt> file.
    :param og: Path to Broccoli result <table_OGs_protein_names.txt> file.
    :param out: Path to output file.
    :param quiet: Specify if output should be quiet.
    :param continuity: Specify if continuity score should be calculated.
    :param overwrite: Specify if output should be overwritten.
    :param ncbi: The NCBI taxonomic database.
    :param dbname: Specify taxadb.sqlite file.
    :return: A list of results such as:
             orthomap, species_list, youngest_common_counts

    :type qt: str
    :type sl: str
    :type og: str
    :type out: str
    :type quiet: bool
    :type continuity: bool
    :type overwrite: bool
    :type ncbi: dict
    :type dbname: str
    :rtype: list

    Example
    -------
    >>> from oggmap import datasets, broccoli2orthomap, of2orthomap, qlin
    >>> datasets.broccoli_example(datapath='.')
    >>> query_orthomap, orthofinder_species_list, of_species_abundance = broccoli2orthomap.get_broccoli_orthomap(
    >>>     seqname='proteome.selected_transcript.ath.fasta',
    >>>     qt='3702',
    >>>     sl='broccoli_example_species_list.tsv',
    >>>     oc='broccoli_example_table_OGs_protein_counts.txt',
    >>>     og='broccoli_example_table_OGs_protein_names.txt',
    >>>     out=None,
    >>>     quiet=False,
    >>>     continuity=True,
    >>>     overwrite=True,
    >>>     dbname='taxadb.sqlite')
    >>> query_orthomap
    """
    outhandle = None
    og_continuity_score = None
    ncbi = qlin.load_taxadb(ncbi=ncbi,
                            dbname=dbname)
    qname,\
        qtid,\
        qlineage,\
        qlineagenames_dict,\
        qlineagezip,\
        qlineagenames,\
        qlineagerev,\
        qk = qlin.get_qlin(qt=qt,
                           quiet=True,
                           ncbi=ncbi)
    query_lineage_topo = qlin.get_lineage_topo(qt=qt,
                                               ncbi=ncbi)
    species_list = pd.read_csv(sl,
                               sep='\t',
                               header=None,
                               comment='#')
    species_list.columns = ['species', 'taxID']
    species_list['lineage'] = species_list.apply(lambda x: qlin.ncbi_get_lineage(qt=x.iloc[1],
                                                                                 ncbi=ncbi),
                                                 axis=1)
    species_list['youngest_common'] = [qlin.get_youngest_common(qlineage, x) for x in species_list.lineage]
    species_list['youngest_name'] = [list(x.values())[0] for x in [qlin.ncbi_get_taxid_translator(qt_vec=[x],
                                                                                                  ncbi=ncbi)
                                                                   for x in list(species_list.youngest_common)]]
    if not quiet:
        print(seqname)
        print(qname)
        print(qt)
        print(species_list)
    youngest_common_counts_df = of2orthomap.get_youngest_common_counts(qlineage,
                                                                       species_list)
    for node in qlin.traverse_postorder(query_lineage_topo.root):
        if node.name:
            nsplit = node.name.split('/')
            if len(nsplit) == 3:
                node.species_count = list(youngest_common_counts_df[youngest_common_counts_df.PStaxID.isin(
                    [int(nsplit[1])])].counts)[0]
    oc_og_dict = {}
    continuity_dict = {}
    if os.path.basename(oc).split('.')[-1] == 'zip':
        oc_zip = zipfile.Path(oc, at='.'.join(os.path.basename(oc).split('.')[:-1]))
        oc_lines = oc_zip.open()
    else:
        oc_lines = open(oc,
                        'r')
    oc_species = next(oc_lines)
    if type(oc_species) == bytes:
        oc_species = oc_species.decode('utf-8').strip().split('\t')
    else:
        oc_species = oc_species.strip().split('\t')
    oc_qidx = [x for x, y in enumerate(oc_species) if y == seqname]
    if len(oc_qidx) == 0:
        print('\nError <-qname>: query species name not in Broccoli results, please check spelling\n'
              'e.g. <head -1 table_OGs_protein_counts.txt>')
        sys.exit()
    for oc_line in oc_lines:
        if type(oc_line) == bytes:
            oc_og = oc_line.decode('utf-8').strip().split('\t')
        else:
            oc_og = oc_line.strip().split('\t')
        if int(oc_og[oc_qidx[0]]) == 0:
            continue
        if int(oc_og[oc_qidx[0]]) > 0:
            oc_og_hits = [oc_species[x+1] for x, y in enumerate(oc_og[1::][::-1][1::][::-1]) if int(y) > 0]
            # get list of the youngest common between query and all other species
            oc_og_hits_youngest_common = list(species_list.youngest_common[
                                                  [x for x, y in enumerate(species_list.species)
                                                   if y in oc_og_hits]])
            # evaluate all youngest common nodes to retain the oldest of them and assign as the orthogroup
            # ancestral state (gene age)
            if len(oc_og_hits_youngest_common) > 0:
                oc_og_oldest_common = qlin.get_oldest_common(qlineage,
                                                             oc_og_hits_youngest_common)
                oc_og_dict[oc_og[0]] = oc_og_oldest_common
                if continuity:
                    continuity_dict[oc_og[0]] = of2orthomap.get_youngest_common_counts(
                        qlineage,
                        pd.DataFrame(oc_og_hits_youngest_common,
                                     columns=['youngest_common'])).counts
    oc_lines.close()
    if continuity:
        youngest_common_counts_df = youngest_common_counts_df.join(pd.DataFrame.from_dict(continuity_dict))
    omap = []
    if out:
        if os.path.exists(out) and not overwrite:
            print('\nError <-overwrite>: output file exists, please set to True if it should be overwritten\n')
            sys.exit()
        outhandle = open(out,
                         'w')
        if continuity:
            outhandle.write('seqID\tOrthogroup\tPSnum\tPStaxID\tPSname\tPScontinuity\n')
        else:
            outhandle.write('seqID\tOrthogroup\tPSnum\tPStaxID\tPSname\n')
    if os.path.basename(og).split('.')[-1] == 'zip':
        og_zip = zipfile.Path(og,
                              at='.'.join(os.path.basename(og).split('.')[:-1]))
        og_lines = og_zip.open()
    else:
        og_lines = open(og,
                        'r')
    og_species = next(og_lines)
    if type(og_species) == bytes:
        og_species = og_species.decode('utf-8').strip().split('\t')
    else:
        og_species = og_species.strip().split('\t')
    og_qidx = [x for x, y in enumerate(og_species) if y == seqname]
    if len(oc_qidx) == 0:
        print('\nError <-qname>: query species name not in Broccoli results, please check spelling\n'
              'e.g. <head -1 table_OGs_protein_counts.txt>')
        sys.exit()
    for og_line in og_lines:
        if type(og_line) == bytes:
            og_og = og_line.decode('utf-8').strip().split('\t')
        else:
            og_og = og_line.strip().split('\t')
        if og_og[0] not in oc_og_dict:
            continue
        else:
            og_ps = qlineagenames[qlineagenames['PStaxID'] ==
                                  str(oc_og_dict[og_og[0]])].values.tolist()[0]
            og_ps_join = '\t'.join(og_ps)
            if continuity:
                og_continuity_score = of2orthomap.get_continuity_score(og_name=og_og[0],
                                                                       youngest_common_counts_df=youngest_common_counts_df)
            if out:
                if continuity:
                    [outhandle.write(x.replace(' ', '') + '\t' + og_og[0] + '\t' + og_ps_join + '\t' +
                                     str(og_continuity_score) + '\n') for x in og_og[og_qidx[0]].split(',')]
                else:
                    [outhandle.write(x.replace(' ', '') + '\t' + og_og[0] + '\t' + og_ps_join + '\n')
                     for x in og_og[og_qidx[0]].split(',')]
        if continuity:
            omap += [[x.replace(' ', ''), og_og[0], og_ps[0], og_ps[1], og_ps[2], og_continuity_score]
                     for x in og_og[og_qidx[0]].split(',')]
        else:
            omap += [[x.replace(' ', ''), og_og[0], og_ps[0], og_ps[1], og_ps[2]]
                     for x in og_og[og_qidx[0]].split(',')]
    og_lines.close()
    if out:
        outhandle.close()
    omap_df = pd.DataFrame(omap)
    if continuity:
        omap_df.columns = ['seqID',
                           'Orthogroup',
                           'PSnum',
                           'PStaxID',
                           'PSname',
                           'PScontinuity']
    else:
        omap_df.columns = ['seqID',
                           'Orthogroup',
                           'PSnum',
                           'PStaxID',
                           'PSname']
    omap_df['PSnum'] = [int(x) for x in list(omap_df['PSnum'])]
    return [omap_df,
            species_list,
            youngest_common_counts_df]


def main():
    """
    The main function that is being called when `plaza2orthomap` is used via the terminal.
    """
    parser = define_parser()
    args = parser.parse_args()
    print(args)
    if not args.dbname:
        print('\nError <-dbname>: Please specify taxadb.sqlite file')
        sys.exit()
    if not args.seqname:
        parser.print_help()
        print('\nError <-seqname>: Please specify query species name in Broccoli and taxID')
        sys.exit()
    if not args.qt:
        parser.print_help()
        print('\nError <-qt>: Please specify query species taxID')
        sys.exit()
    if not args.sl:
        parser.print_help()
        print('\nError <-sl>: Please specify species list as <Broccoli name><tab><species taxID>')
        sys.exit()
    if not args.oc:
        parser.print_help()
        print('\nError <-oc>: Please specify Broccoli <table_OGs_protein_counts.txt> (see dir_step3 directory)')
        sys.exit()
    if not args.og:
        parser.print_help()
        print('\nError <-og>: Please specify Broccoli <table_OGs_protein_names.txt> (see dir_step3 directory)')
        sys.exit()
    get_broccoli_orthomap(seqname=args.seqname,
                          qt=args.qt,
                          sl=args.sl,
                          oc=args.oc,
                          og=args.og,
                          out=args.out,
                          quiet=False,
                          continuity=True,
                          overwrite=args.overwrite,
                          dbname=args.dbname)


if __name__ == '__main__':
    main()
