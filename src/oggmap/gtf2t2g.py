#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
Author: Kristian K Ullrich
date: April 2023
email: ullrich@evolbio.mpg.de
License: GPL-3
"""


import os
import sys
import argparse
import gzip
import pandas as pd


def define_parser():
    """
    A helper function for using `gtf2t2g.py` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    gtf2t2g_example = '''gtf2t2g example:
    
    # to get GTF from Mus musculus on Linux run:
    $ wget https://ftp.ensembl.org/pub/release-108/gtf/mus_musculus/Mus_musculus.GRCm39.108.chr.gtf.gz

    # on Mac:
    $ curl https://ftp.ensembl.org/pub/release-108/gtf/mus_musculus/Mus_musculus.GRCm39.108.chr.gtf.gz --remote-name

    # create t2g from GTF:
    $ gtf2t2g -i Mus_musculus.GRCm39.108.chr.gtf.gz -o Mus_musculus.GRCm39.108.chr.gtf.t2g.tsv -g -b -p -v -s
    '''
    parser = argparse.ArgumentParser(
        prog='gtf2t2g',
        usage='%(prog)s [options] [<arguments>...]',
        description='extract transcript to gene table from GTF',
        epilog=gtf2t2g_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_argparse_args(parser=parser)
    return parser


def add_argparse_args(parser: argparse.ArgumentParser):
    """
    This function attaches individual argument specifications to the parser.

    :param parser: An argparse.ArgumentParser.

    :type parser: argparse.ArgumentParser
    """
    parser.add_argument('-i',
                        help='specify GTF input file')
    parser.add_argument('-o',
                        help='specify output file [optional]')
    parser.add_argument('-g',
                        help='specify if gene names should be appended if they exist',
                        action='store_true')
    parser.add_argument('-b',
                        help='specify if gene biotype should be appended if they exist',
                        action='store_true')
    parser.add_argument('-p',
                        help='specify if protein id should be appended if they exist',
                        action='store_true')
    parser.add_argument('-v',
                        help='specify if gene/transcript/protein version should be appended',
                        action='store_true')
    parser.add_argument('-s',
                        help='specify if summary should be printed',
                        action='store_true')
    parser.add_argument('-q',
                        help='specify if output should be quite',
                        action='store_true')
    parser.add_argument('-overwrite',
                        help='specify if existing output file should be overwritten (default: True)',
                        default=True,
                        type=bool)


def _information_based_on_key(infosplit,
                              key,
                              q,
                              lines,
                              version=False):
    """
    A helper function to split the information column of GTF file.

    :param infosplit: Split information column of GTF file.
    :param key: Keyword.
    :param q: Specify if output should be quiet.
    :param lines: Line of GTF file.
    :param version: Specify if gene/transcript/protein version should be appended.
    :return: A list of parsed information from a GTF info field such as:
             infos, output

    :type infosplit: list
    :type key: str
    :type q: bool
    :type lines: str
    :type version: bool
    :rtype: list

    Example
    -------
    >>>
    """
    output = None
    if version:
        infos = [x for x in infosplit if key in x and f'havana_{key}' not in x]
    else:
        infos = [x for x in infosplit if key in x]
    if infos:
        if len(infos) == 1:
            output = infos[0]
            output = output.replace(key, '').replace(' ', '').replace('"', '')
        else:
            if not q:
                print(f'duplicated {key} field:\t' + lines)
    else:
        if not q:
            print(f'no {key} field:\t' + lines)
    return [infos, output]


def parse_gtf(gtf,
              g=False,
              b=False,
              p=False,
              v=False,
              s=False,
              output=None,
              q=False):
    """
    This function parses a GTF file to extract transcript and gene IDs.

    :param gtf: Path to GTF file.
    :param g: Specify if gene names should be appended if they exist.
    :param b: Specify if gene biotype should be appended if they exist.
    :param p: Specify if protein id should be appended if they exist.
    :param v: Specify if gene/transcript/protein version should be appended.
    :param s: Specify if summary should be printed.
    :param output: File object.
    :param q: Specify if output should be quiet.
    :return: DataFrame with transcript and gene IDs.

    :type gtf: str
    :type g: bool
    :type b: bool
    :type p: bool
    :type v: bool
    :type s: bool
    :type output: file object
    :type q: bool
    :rtype: pandas.DataFrame

    Example
    -------
    >>> from oggmap import datasets, gtf2t2g
    >>> # get gene to transcript table for Danio rerio
    >>> # https://ftp.ensembl.org/pub/release-105/gtf/danio_rerio/Danio_rerio.GRCz11.105.gtf.gz
    >>> gtf_file = datasets.zebrafish_gtf(datapath='.')
    >>> query_species_t2g = gtf2t2g.parse_gtf(gtf=gtf_file,\
    >>>     g=True, b=True, p=True, v=True, s=True, q=True)
    >>> query_species_t2g
    """
    if gtf.endswith('gz'):
        gtf_handle = gzip.open(gtf,
                               'rt')
    else:
        gtf_handle = open(gtf,
                          'rt')
    t2g = {}
    t2p = {}
    tc = 0
    gc = 0
    pc = 0
    dc = 0
    for lines in gtf_handle:
        if len(lines) == 0 or lines[0] == '#':
            continue
        line = lines.strip().split('\t')
        if line[2] == 'transcript':
            gname_first = None
            gtype_first = None
            gid_first_version = None
            tid_first_version = None
            infosplit = line[8].strip().split(';')
            gid, gid_first = _information_based_on_key(infosplit=infosplit,
                                                       key='gene_id',
                                                       q=q,
                                                       lines=lines)
            if not gid:
                continue
            tid, tid_first = _information_based_on_key(infosplit=infosplit,
                                                       key='transcript_id',
                                                       q=q,
                                                       lines=lines)
            if not tid:
                continue
            if g:
                _, gname_first = _information_based_on_key(infosplit=infosplit,
                                                           key='gene_name',
                                                           q=q,
                                                           lines=lines)
            if b:
                _, gtype_first = _information_based_on_key(infosplit=infosplit,
                                                           key='gene_biotype',
                                                           q=q,
                                                           lines=lines)
            if v:
                _, gv_first = _information_based_on_key(infosplit=infosplit,
                                                        key='gene_version',
                                                        q=q,
                                                        lines=line,
                                                        version=True)
                _, tv_first = _information_based_on_key(infosplit=infosplit,
                                                        key='transcript_version',
                                                        q=q,
                                                        lines=line,
                                                        version=True)
                if gv_first:
                    gid_first_version = gid_first + '.' + gv_first
                if tv_first:
                    tid_first_version = tid_first + '.' + tv_first
            if gid_first in t2g:
                if tid_first in t2g[gid_first]:
                    dc += 1
                    if not q:
                        print('duplicated gid-tid: ' + gid_first + ' ' + tid_first)
                    continue
                if tid_first not in t2g[gid_first]:
                    tc += 1
                    t2g[gid_first][tid_first] = [
                        gid_first,
                        gid_first_version,
                        tid_first,
                        tid_first_version,
                        gname_first,
                        gtype_first, ]
            if gid_first not in t2g:
                gc += 1
                tc += 1
                t2g[gid_first] = {}
                t2g[gid_first][tid_first] = [
                    gid_first,
                    gid_first_version,
                    tid_first,
                    tid_first_version,
                    gname_first,
                    gtype_first, ]
        if line[2] == 'CDS':
            if p:
                pid_first = None
                pid_first_version = None
                tid_first = None
                pv_first = None
                infosplit = line[8].strip().split(';')
                tid, tid_first = _information_based_on_key(infosplit=infosplit,
                                                           key='transcript_id',
                                                           q=q,
                                                           lines=lines)
                tid = [x for x in infosplit if 'transcript_id' in x]
                if not tid:
                    continue
                pid, pid_first = _information_based_on_key(infosplit=infosplit,
                                                           key='protein_id',
                                                           q=q,
                                                           lines=lines)
                if not pid:
                    continue
                if v:
                    _, pv_first = _information_based_on_key(infosplit=infosplit,
                                                            key='protein_version',
                                                            q=q,
                                                            lines=lines)
                    if pv_first:
                        pid_first_version = pid_first + '.' + pv_first
                if tid_first in t2p:
                    continue
                if tid_first not in t2p:
                    pc += 1
                    t2p[tid_first] = [pid_first, pid_first_version]
    for gidk in sorted(t2g.keys()):
        for tidk in sorted(t2g[gidk].keys()):
            pidk = None
            pidk_v = None
            if tidk in t2p:
                pidk = t2p[tidk][0]
                pidk_v = t2p[tidk][1]
            t2g[gidk][tidk] = t2g[gidk][tidk] + [pidk, pidk_v]
            if output:
                output.write('\t'.join([str(x) for x in t2g[gidk][tidk]]) + '\n')
    if s:
        summary_text = f"""{str(gc)} gene_id found
{str(tc)} transcript_id found
{str(tc)} protein_id found
{str(dc)} duplicated"""
        print(summary_text)
    t2g_df = pd.DataFrame.from_dict(
        {(i, j): t2g[i][j] for i in t2g.keys() for j in t2g[i].keys()},
        orient='index',
        columns=[
            'gene_id',
            'gene_id_version',
            'transcript_id',
            'transcript_id_version',
            'gene_name',
            'gene_type',
            'protein_id',
            'protein_id_version', ], )
    t2g_df.sort_values(by='gene_id',
                       inplace=True)
    t2g_df.reset_index(drop=True,
                       inplace=True)
    gtf_handle.close()
    return t2g_df


def main():
    """
    The main function that is being called when `gtf2t2g` is used via the terminal.
    """
    parser = define_parser()
    args = parser.parse_args()
    print(args)
    if not args.i:
        parser.print_help()
        print('\nError <-i>: Please specify GTF input file')
        sys.exit()
    if args.o:
        if os.path.exists(args.o) and not args.overwrite:
            print('\nError <-overwrite>: output file exists, please set to True if it should be overwritten\n')
            sys.exit()
        output = open(args.o, 'w')
    else:
        output = sys.stdout
    parse_gtf(gtf=args.i,
              g=args.g,
              b=args.b,
              p=args.p,
              v=args.v,
              s=args.s,
              output=output,
              q=args.q)
    output.close()


if __name__ == '__main__':
    main()
