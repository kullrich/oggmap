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
import argparse
import pandas as pd
from taxadb2.taxid import TaxID
from taxadb2.names import SciName
from Bio import Phylo
from io import StringIO


def define_parser():
    """
    A helper function for using `qlin.py` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    qlin_example = '''qlin example:

    # get query lineage to be used with oggmap later on using query species taxID
    # Mus musculus; 10090
    $ qlin -qt 10090 -dbname taxadb.sqlite

    # using query species name
    $ qlin -q "Mus musculus" -dbname taxadb.sqlite
    '''
    parser = argparse.ArgumentParser(
        prog='qlin',
        usage='%(prog)s [options] [<arguments>...]',
        description='get query lineage based on ncbi taxonomy',
        epilog=qlin_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_argparse_args(parser=parser)
    return parser


def add_argparse_args(parser: argparse.ArgumentParser):
    """
    This function attaches individual argument specifications to the parser.

    :param parser: An argparse.ArgumentParser.

    :type parser: argparse.ArgumentParser
    """
    parser.add_argument('-q',
                        help='query species name')
    parser.add_argument('-qt',
                        help='query species taxID')
    parser.add_argument('-dbname',
                        help='taxadb.sqlite file')

def traverse_postorder(clade):
    """
    Yield each clade (node) in a post-order traversal (children before parent)

    :param clade: A Clade object from a Bio.Phylo.Newick.Tree.

    :type clade: Bio.Phylo.Newick.Clade
    """
    if hasattr(clade, "clades"):
        for child in clade.clades:
            yield from traverse_postorder(child)
    yield clade


def load_taxadb(ncbi, dbname):
    """
    Load taxadb.sqlite database or exit if neither ncbi nor dbname are provided.

    :param ncbi: Existing ncbi dictionary, if any.
    :param dbname: Path to taxadb.sqlite file.

    :rtype: dict
    """
    if ncbi is None and dbname is None:
        sys.exit('\nPlease provide path to taxadb.sqlite file')
    if ncbi is None and dbname is not None:
        if not os.path.exists(dbname):
            raise FileNotFoundError(f"Database file '{dbname}' not found.")
        ncbi = {
            'taxid': TaxID(dbtype='sqlite', dbname=dbname),
            'names': SciName(dbtype='sqlite', dbname=dbname)
        }
    return ncbi


def ncbi_get_lineage(qt,
                     ncbi=None,
                     dbname=None):
    """
    This function returns a species lineage for a query species given as taxID.

    :param qt: The taxID of the queried species.
    :param ncbi: The NCBI taxonomic database.
    :param dbname: Specify taxadb.sqlite file.

    :type qt: str
    :type ncbi: dict
    :type dbname: str
    :rtype: list
    """
    ncbi = load_taxadb(ncbi=ncbi, dbname=dbname)
    taxid2name = ncbi['taxid'].sci_name(qt)
    qtid = ncbi['names'].taxid(taxid2name)
    qlineage = [1] + ncbi['taxid'].lineage_id(qtid, reverse=True)
    return qlineage


def ncbi_get_taxid_translator(qt_vec,
                              ncbi=None,
                              dbname=None):
    """
    This function returns a dictionary for a vector of taxIDs as integers.

    :param qt_vec: A vector of taxIDs as integers.
    :param ncbi: The NCBI taxonomic database.
    :param dbname: Specify taxadb.sqlite file.

    :type qt_vec: list of int
    :type ncbi: dict
    :type dbname: str
    :rtype: dict
    """
    ncbi = load_taxadb(ncbi=ncbi, dbname=dbname)
    if not isinstance(qt_vec, list):
        sys.exit('\nqt_vec needs to be a vector of taxIDs as integers')
    else:
        qt_vec = [int(x) for x in qt_vec]
    taxid2names = [ncbi['taxid'].sci_name(qt) for qt in qt_vec]
    qtids = [ncbi['names'].taxid(taxid2name) for taxid2name in taxid2names]
    translations = dict(zip(qtids, taxid2names))
    return translations


def get_qlin(q=None,
             qt=None,
             quiet=False,
             ncbi=None,
             dbname=None):
    """
    This function searches the NCBI taxonomic database for results matching the
    query name or query taxID.

    Note that if the user specifies both the name and the taxID of a species,
    the returning result is based on the taxID.

    :param q: The name of the queried species.
    :param qt: The taxID of the queried species.
    :param quiet: Specify if output should be quiet.
    :param ncbi: The NCBI taxonomic database.
    :param dbname: Specify taxadb.sqlite file.
    :return: A list of information for the queried species such as:
             query name, query taxID, query lineage, query lineage dictionary, query lineage zip,
             query lineage names, reverse query lineage, query kingdom

    :type q: str
    :type qt: str
    :type quiet: bool
    :type ncbi: dict
    :type dbname: str
    :rtype: list

    Example
    -------
    >>> from oggmap import qlin
    >>> qlin.get_qlin(q='Danio rerio',
    >>>               dbname='taxadb.sqlite')
    """
    ncbi = load_taxadb(ncbi=ncbi, dbname=dbname)
    qtid = None
    qname = None
    qk = None
    #if ncbi is None:
        #ncbi = NCBITaxa()
    if qt:
        #taxid2name = ncbi.get_taxid_translator([int(qt)])
        #taxid2name = taxid.sci_name(qt)
        taxid2name = ncbi['taxid'].sci_name(qt)
        #qtid, \
        #    qname = list(taxid2name.items())[0]
        #qtid = names.taxid(taxid2name)
        qtid = ncbi['names'].taxid(taxid2name)
        qname = taxid2name
    if q and not qt:
        #name2taxid = ncbi.get_name_translator([q])
        #name2taxid = names.taxid(q)
        name2taxid = ncbi['names'].taxid(q)
        #qname, \
        #    qtid = list(name2taxid.items())[0]
        #qtid = qtid[0]
        #qname = taxid.sci_name(name2taxid)
        qname = ncbi['taxid'].sci_name(name2taxid)
        qtid = name2taxid
    #qlineage = ncbi.get_lineage(qtid)
    #qlineage = [1]+taxid.lineage_id(qtid, reverse=True)
    qlineage = [1] + ncbi['taxid'].lineage_id(qtid, reverse=True)
    #qlineagen = ['root'] + taxid.lineage_name(qtid, reverse=True)
    qlineagen = ['root'] + ncbi['taxid'].lineage_name(qtid, reverse=True)
    #qlineagenames_dict = ncbi.get_taxid_translator(qlineage)
    qlineagenames_dict = dict(zip(qlineage, qlineagen))
    qlineagezip = [(a, qlineagenames_dict[a]) for a in qlineage]
    qlineagenames = pd.DataFrame([(x, y, qlineagenames_dict[y]) for x, y in enumerate(qlineage)],
                                 columns=['PSnum',
                                          'PStaxID',
                                          'PSname'])
    qlineagenames['PSnum'] = [str(x) for x in list(qlineagenames['PSnum'])]
    qlineagenames['PStaxID'] = [str(x) for x in list(qlineagenames['PStaxID'])]
    qlineagenames['PSname'] = [str(x) for x in list(qlineagenames['PSname'])]
    qlineagerev = qlineage[::-1]
    if qlineage[2] == 2:
        qk = 'Bacteria'
    if qlineage[2] == 2157:
        qk = 'Archea'
    if qlineage[2] == 2759:
        qk = 'Eukaryota'
    if not quiet:
        print('query name: %s' % qname)
        print('query taxID: %s' % str(qtid))
        print('query kingdom: %s' % qk)
        print(
            'query lineage names: \n%s' % str([qlineagenames_dict[x] + '(' + str(x) + ')' for x in qlineage])
        )
        print('query lineage: \n%s' % str(qlineage))
    return [qname,
            qtid,
            qlineage,
            qlineagenames_dict,
            qlineagezip,
            qlineagenames,
            qlineagerev,
            qk]


def get_lineage_topo(qt,
                     ncbi=None,
                     dbname=None):
    """
    This function returns a species lineage as a tree object for a query species given as taxID.

    :param qt: The taxID of the queried species.
    :param ncbi: The NCBI taxonomic database.
    :param dbname: Specify taxadb.sqlite file.
    :return: The lineage of the queried species as a Bio.Phylo.Newick.Tree.

    :type qt: str
    :type ncbi: dict
    :type dbname: str
    :rtype: Bio.Phylo.Newick.Tree

    Example
    -------
    >>> from oggmap import qlin
    >>> lineage_tree = qlin.get_lineage_topo(qt='10090',
    >>>                                      dbname='taxadb.sqlite')
    >>> lineage_tree
    """
    _, _, _, _, _, qlineagenames, _, _ = get_qlin(qt=qt,
                                                  quiet=True,
                                                  ncbi=ncbi,
                                                  dbname=dbname)
    qln = list(qlineagenames[['PSnum',
                              'PStaxID',
                              'PSname']].apply(lambda x: '/'.join(x), axis=1))
    qln = [x.replace('(', '_').replace(')', '_').replace(':', '_') for x in qln]
    #tree = Tree('(' * len(qln) + ''.join([str(x) + '),' for x in qln[1::][::-1]])+str(qln[0])+');')
    newick_str = '(' * len(qln) + ''.join([str(x) + '),' for x in qln[1::][::-1]]) + str(qln[0]) + ');'
    tree = Phylo.read(StringIO(newick_str), 'newick')
    return tree


def get_youngest_common(ql,
                        tl):
    """
    This function returns the lowest common ancestor (LCA) by comparing the lineage information
    of a query and a target species.

    :param ql: Query species lineage information.
    :param tl: Target species lineage information.
    :return: lowest common ancestor (LCA).

    :type ql: list
    :type tl: list
    :rtype: str

    Example
    -------
    >>> from oggmap import qlin
    >>> # get query species taxonomic lineage information
    >>> _, _, query_lineage, _, _, _, _, _ = qlin.get_qlin(q='Caenorhabditis elegans',
    >>>                                                    dbname='taxadb.sqlite')
    >>> # get target species taxonomic lineage information
    >>> _, _, target_lineage, _, _, _, _, _ = qlin.get_qlin(q='Mus musculus',
    >>>                                                     dbname='taxadb.sqlite')
    >>> # get youngest common node
    >>> qlin.get_youngest_common(ql=query_lineage, tl=target_lineage)
    """
    return [x for x in tl if x in ql][-1]


def get_oldest_common(ql,
                      tl):
    """
    This function returns the oldest common ancestor (OCA) by comparing the lineage information
    of a query species and a target species.

    The target species can also be a list of LCA values to find the oldest among the given LCA.

    :param ql: Query species lineage information.
    :param tl: Target species lineage information.
    :return: oldest common ancestor (OCA).

    :type ql: list
    :type tl: list
    :rtype: str

    Example
    -------
    >>> from oggmap import qlin
    >>> # get query species taxonomic lineage information
    >>> _, _, query_lineage, _, _, _, _, _ = qlin.get_qlin(q='Caenorhabditis elegans',
    >>>                                                    dbname='taxadb.sqlite')
    >>> # get target species taxonomic lineage information
    >>> _, _, target_lineage, _, _, _, _, _ = qlin.get_qlin(q='Mus musculus',
    >>>                                                     dbname='taxadb.sqlite')
    >>> # get oldest common node
    >>> qlin.get_oldest_common(ql=query_lineage, tl=target_lineage)
    """
    return ql[min([x for x, y in enumerate(ql) if y in tl])]


def main():
    """
    The main function that is being called when `qlin` is used via the terminal.
    """
    parser = define_parser()
    args = parser.parse_args()
    print(args)
    if not args.dbname:
        print('\nError <-dbname> : Please specify taxadb.sqlite file')
        sys.exit()
    if not args.q and not args.qt:
        parser.print_help()
        print('\nError <-q> <-qt>: Please specify query species name or taxID')
        sys.exit()
    if args.q and args.qt:
        parser.print_help()
        print('\nWarning: Since both query species name and taxID are given taxID is used')
        sys.exit()
    get_qlin(q=args.q,
             qt=args.qt,
             quiet=False,
             dbname=args.dbname)


if __name__ == '__main__':
    main()
