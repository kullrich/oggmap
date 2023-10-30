#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
Author: Kristian K Ullrich
date: May 2023
email: ullrich@evolbio.mpg.de
License: GPL-3
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from oggmap import of2orthomap, qlin
from ete3 import NCBITaxa


def define_parser():
    """
    A helper function for using `orthomcl2orthomap.py` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    orthomcl2orthomap_example = '''example:

    # quickly find 'Arabidopsis thaliana' short name
    # grep 'Arabidopsis thaliana' genomeSummary_OrthoMCL-6.16.txt
    
    # extract orthomap:
    $ orthomcl2orthomap -tla atha -sl genomeSummary_OrthoMCL-6.16.txt -og groups_OrthoMCL-6.16.txt -out atha.orthomap
    '''
    parser = argparse.ArgumentParser(
        prog='orthomcl2orthomap',
        usage='%(prog)s [options] [<arguments>...]',
        description='extract orthomap from orthomcl output for query species',
        epilog=orthomcl2orthomap_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_argparse_args(parser=parser)
    return parser


def add_argparse_args(parser: argparse.ArgumentParser):
    """
    This function attaches individual argument specifications to the parser.

    :param parser: An argparse.ArgumentParser.

    :type parser: argparse.ArgumentParser
    """
    parser.add_argument('-tla',
                        help='query species orthomcl short name (THREE_LETTER_ABBREV)')
    parser.add_argument('-sl',
                        help='specify orthomcl species information file <genomeSummary_OrthoMCL-6.16.txt>')
    parser.add_argument('-og',
                        help='specify orthomcl groups file <groups_OrthoMCL-6.16.txt>')
    parser.add_argument('-out',
                        help='specify output file <orthomap.tsv> (default: orthomap.tsv)',
                        default='orthomap.tsv')
    parser.add_argument('-overwrite',
                        help='specify if existing output file should be overwritten (default: True)',
                        default=True,
                        type=bool)


def _get_species_tax_id(species_name_list, species_list):
    """
    A helper function to map orthomcl species short name and species taxID.

    :param species_name_list: List of orthomcl species short names.
    :param species_list: DataFrame with orthomcl species information.
    :return: List of species taxID.

    :type species_name_list: list
    :type species_list: pandas.DataFrame
    :rtype: list
    """
    species_taxid_list = []
    for species_name in species_name_list:
        species_taxid = list(species_list['tax_id'][species_list['THREE_LETTER_ABBREV'] == species_name])
        if len(species_taxid) > 0:
            species_taxid_list.append(species_taxid[0])
    return species_taxid_list


def _parse_orthomcl_groups(og, tla):
    """
    A helper function to parse orthomcl groups.

    :param og: Path to orthomcl groups <groups_OrthoMCL-6.16.txt> file.
    :param tla: Query species orthomcl short name (THREE_LETTER_ABBREV).
    :return: DataFrame.

    :type og: string
    :type tla: string
    :rtype:  pandas.DataFrame
    """
    ogs_gf_id = []
    ogs_species = []
    ogs_gene_id = []
    with open(og, 'rt') as og_handle:
        for og_line in og_handle:
            if tla + '|' in og_line:
                og_line_split = og_line.strip().split(' ')
                og_line_group = og_line_split[0].replace(':', '')
                for og_hit in og_line_split[1:]:
                    species, gene = og_hit.split('|')
                    ogs_gf_id += [og_line_group]
                    ogs_species += [species]
                    ogs_gene_id += [gene]
    ogs = pd.DataFrame([ogs_gf_id, ogs_species, ogs_gene_id]).transpose()
    ogs.columns = ['gf_id', 'species', 'gene_id']
    return ogs


def get_orthomcl_orthomap(tla,
                          sl,
                          og,
                          out=None,
                          quiet=False,
                          continuity=True,
                          overwrite=True):
    """
    This function return an orthomap for a given query species and orthomcl groups data.

    :param tla: Query species orthomcl short name (THREE_LETTER_ABBREV).
    :param sl: Path to orthomcl species information <genomeSummary_OrthoMCL-6.16.txt> file.
    :param og: Path to orthomcl groups <groups_OrthoMCL-6.16.txt> file.
    :param out: Path to output file.
    :param quiet: Specify if output should be quiet.
    :param continuity: Specify if continuity score should be calculated.
    :param overwrite: Specify if output should be overwritten.
    :return: A list of results such as:
             orthomap, species_list, youngest_common_counts

    :type tla: str
    :type sl: str
    :type og: str
    :type out: str
    :type quiet: bool
    :type continuity: bool
    :type overwrite: bool
    :rtype: list

    Example
    -------
    >>>
    """
    outhandle = None
    og_continuity_score = None
    ncbi = NCBITaxa()
    species_list = pd.read_csv(sl, sep='\t', header=0, comment='#')
    if tla not in list(species_list['THREE_LETTER_ABBREV']):
        print('\nError <-qt>: query species orthomcl short name not in orthomcl results,'
              'please check THREE_LETTER_ABBREV.')
        sys.exit()
    species_list['species'] = [' '.join(x.split(' ')[:2])
                               .replace('Ashbya gossypii', 'Eremothecium gossypii')
                               .replace('Amphiamblys sp.', 'Amphiamblys')
                               .replace('Candida haemulonis', '[Candida] cf. haemuloni HMD-2015')
                               .replace('Candida pseudohaemulonii', '[Candida] pseudohaemulonii')
                               .replace('Cryptococcus cf.', 'Cryptococcus cf. gattii')
                               .replace('Giardia Assemblage', 'Giardia intestinalis')
                               .replace('Melampsora larici-populina', 'Melampsora laricis-populina')
                               .replace('Nematocida ironsii', 'Nematocida')
                               .replace('Plasmodium adleri', 'Plasmodium (Laverania)')
                               .replace('Plasmodium blacklocki', 'Plasmodium (Laverania)')
                               .replace('Plasmodium praefalciparum', 'Plasmodium (Laverania)')
                               .replace('Plasmodium vivax-like', 'Plasmodium (Laverania)')
                               .replace('Porospora cf.', 'Porospora')
                               for x in species_list['NAME']]
    species_list['tax_id'] = [qlin.get_qlin(q=x, quiet=True)[1] for x in species_list['species']]
    qt_species = list(species_list[species_list['THREE_LETTER_ABBREV'] == tla]['tax_id'])[0]
    qname,\
        qtid,\
        qlineage,\
        qlineagenames_dict,\
        qlineagezip,\
        qlineagenames,\
        qlineagerev,\
        qk = qlin.get_qlin(qt=qt_species,
                           quiet=True)
    query_lineage_topo = qlin.get_lineage_topo(qt_species)
    ogs = _parse_orthomcl_groups(og, tla)
    ogs_grouped = ogs.groupby('gf_id')['species'].apply(set).apply(list).apply(_get_species_tax_id,
                                                                               species_list=species_list)
    ogs_grouped_qt = pd.DataFrame(ogs_grouped[ogs_grouped.apply(lambda x: int(qt_species) in x)])
    ogs_qt = ogs[ogs['gf_id'].isin(ogs_grouped_qt.index)]
    ogs_qt_red = ogs_qt[ogs_qt['species'].isin([tla])]
    ogs_qt_red_grouped = ogs_qt_red.groupby('gf_id')['gene_id'].apply(list)
    ogs_grouped_qt['gene_id'] = ogs_qt_red_grouped
    ogs_grouped_qt_species = np.sort(list(set([x[0] for x in ogs_grouped_qt['species'].to_dict().values()])))
    ogs_grouped_qt_species_names = [qlin.get_qlin(qt=x,
                                                  quiet=True)[0] for x in ogs_grouped_qt_species]
    species_list_df = pd.DataFrame(ogs_grouped_qt_species_names,
                                   columns=['species'])
    species_list_df['taxID'] = ogs_grouped_qt_species
    species_list_df['lineage'] = species_list_df.apply(lambda x: ncbi.get_lineage(x[1]),
                                                       axis=1)
    species_list_df['youngest_common'] = [qlin.get_youngest_common(qlineage,
                                                                   x) for x in species_list_df.lineage]
    species_list_df['youngest_name'] = [list(x.values())[0] for x in [ncbi.get_taxid_translator([x])
                                                                      for x in list(species_list_df.youngest_common)]]
    if not quiet:
        print(qname)
        print(tla)
        print(species_list_df)
    youngest_common_counts_df = of2orthomap.get_youngest_common_counts(qlineage,
                                                                       species_list_df)
    for node in query_lineage_topo.traverse('postorder'):
        nsplit = node.name.split('/')
        if len(nsplit) == 3:
            node.add_feature('species_count',
                             list(youngest_common_counts_df[youngest_common_counts_df.PStaxID.isin(
                                 [int(nsplit[1])])].counts)[0])
    og_dict = {}
    continuity_dict = {}
    for og in ogs_grouped_qt.index:
        og_hits = np.sort(
            list(set(list(ogs_grouped_qt[ogs_grouped_qt.index.isin([og])]['species'].to_dict().values())[0])))
        # get list of the youngest common between query and all other species
        og_hits_youngest_common = list(species_list_df.youngest_common[
                                           [x for x, y in enumerate(species_list_df.taxID)
                                            if y in og_hits]])
        # evaluate all youngest common nodes to retain the oldest of them and assign as the orthogroup
        # ancestral state (gene age)
        if len(og_hits_youngest_common) > 0:
            og_oldest_common = qlin.get_oldest_common(qlineage,
                                                      og_hits_youngest_common)
            og_dict[og] = og_oldest_common
            if continuity:
                continuity_dict[og] = \
                    of2orthomap.get_youngest_common_counts(qlineage,
                                                           pd.DataFrame(og_hits_youngest_common,
                                                                        columns=['youngest_common'])).counts
    if continuity:
        youngest_common_counts_df = youngest_common_counts_df.join(pd.DataFrame.from_dict(continuity_dict))
    omap = []
    if out:
        if os.path.exists(out) and not overwrite:
            print('\nError <-overwrite>: output file exists, please set to True if it should be overwritten\n')
            sys.exit()
        outhandle = open(out, 'w')
        if continuity:
            outhandle.write('seqID\tOrthogroup\tPSnum\tPStaxID\tPSname\tPScontinuity\n')
        else:
            outhandle.write('seqID\tOrthogroup\tPSnum\tPStaxID\tPSname\n')
    for og in ogs_grouped_qt.index:
        og_tmp = ogs_grouped_qt[ogs_grouped_qt.index.isin([og])]
        og_ps = qlineagenames[qlineagenames['PStaxID'] ==
                              str(og_dict[og])].values.tolist()[0]
        og_ps_join = '\t'.join(og_ps)
        if continuity:
            og_continuity_score = of2orthomap.get_continuity_score(og,
                                                                   youngest_common_counts_df)
            if out:
                if continuity:
                    [outhandle.write(x.replace(' ', '') + '\t' + og + '\t' + og_ps_join + '\t' +
                                     str(og_continuity_score) + '\n') for x in list(og_tmp['gene_id'])[0]]
                else:
                    [outhandle.write(x.replace(' ', '') + '\t' + og + '\t' + og_ps_join + '\n')
                     for x in list(og_tmp['gene_id'])[0]]
        if continuity:
            omap += [[x.replace(' ', ''), og, og_ps[0], og_ps[1], og_ps[2], og_continuity_score]
                     for x in list(og_tmp['gene_id'])[0]]
        else:
            omap += [[x.replace(' ', ''), og, og_ps[0], og_ps[1], og_ps[2]]
                     for x in list(og_tmp['gene_id'])[0]]
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
            species_list_df,
            youngest_common_counts_df]


def main():
    """
    The main function that is being called when `orthomcl2orthomap` is used via the terminal.
    """
    parser = define_parser()
    args = parser.parse_args()
    print(args)
    if not args.tla:
        parser.print_help()
        print('\nError <-tla>: Please specify query species orthomcl short name (THREE_LETTER_ABBREV)')
        sys.exit()
    if not args.sl:
        parser.print_help()
        print('\nError <-sl>: Please specify orthomcl species information file <genomeSummary_OrthoMCL-6.16.txt>')
        sys.exit()
    if not args.og:
        parser.print_help()
        print('\nError <-og>: Please specify orthomcl groups file <groups_OrthoMCL-6.16.txt>')
        sys.exit()
    get_orthomcl_orthomap(tla=args.tla,
                          sl=args.sl,
                          og=args.og,
                          out=args.out,
                          overwrite=args.overwrite)


if __name__ == '__main__':
    main()
