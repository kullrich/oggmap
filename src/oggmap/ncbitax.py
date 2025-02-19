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
from taxadb2 import app


def define_parser():
    """
    A helper function for using `ncbitax.py` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    ncbitax_example = '''ncbitax example:

    #update ncbi taxonomy database:
    ncbitax -u -outdir taxadb -type taxa -dbname taxadb
    '''
    parser = argparse.ArgumentParser(
        prog='ncbitax',
        usage='%(prog)s [options] [<arguments>...]',
        description='update local ncbi taxonomy database', epilog=ncbitax_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_argparse_args(parser=parser)
    return parser


def add_argparse_args(parser: argparse.ArgumentParser):
    """
    This function attaches individual argument specifications to the parser.

    :param parser: An argparse.ArgumentParser.

    :type parser: argparse.ArgumentParser
    """
    parser.add_argument('-u',
                        help='update',
                        action='store_true')
    parser.add_argument('-outdir',
                        help='output directory option for taxadb2 download')
    parser.add_argument('-t',
                        help='type option for taxadb2 download (default: taxa)',
                        default='taxa',
                        type=str)
    parser.add_argument('-dbname',
                        help='dbname option for taxadb2 create (default: taxadb.sqlite)',
                        default='taxadb.sqlite',
                        type=str)
    parser.add_argument('-chunk',
                        help='chunk option for taxadb2 create (default: 500)',
                        default=500,
                        type=int)
    parser.add_argument('-force',
                        help='force option for taxadb2 download (default: False)',
                        action='store_true')
    parser.add_argument('-verbose',
                        help='increase verbosity (default: False)',
                        action='store_true')


def update_ncbi(args):
    """
    This function updates or downloads the NCBI taxonomy database using
    the package `ete3`. A parsed version of it will be stored at the home
    directory: `~/.etetoolkit/taxa.sqlite`.

    :param args: Command-line arguments.

    :type args: argparse.Namespace

    Example
    -------
    >>> from oggmap import ncbitax
    >>> update_parser = ncbitax.define_parser()
    >>> update_args = update_parser.parse_args()
    >>> update_args.outdir = 'taxadb'
    >>> update_args.dbname = 'taxadb.sqlite'
    >>> ncbitax.update_ncbi(update_args)
    """
    #ncbi = NCBITaxa()
    #ncbi.update_taxonomy_database()
    current_dir = os.getcwd()
    args.type = [[args.t]]
    app.download_files(args)
    args.type = [args.t]
    args.input = os.path.abspath(os.getcwd())
    args.dbtype = 'sqlite'
    args.division = args.t
    args.fast = False
    args.verbose = False
    os.chdir(os.path.abspath(current_dir))
    app.create_db(args)


def main():
    """
    The main function that is being called when `ncbitax.py` is used via the terminal.
    """
    parser = define_parser()
    args = parser.parse_args()
    print(args)
    if not args.u:
        parser.print_help()
        print('\nError <-u>: Please specify if you like to update <-u>')
        sys.exit()
    if args.u:
        if not args.outdir:
            parser.print_help()
            print('\nError <-outdir>: Please specify outdir if you like to update <-outdir>')
            sys.exit()
        else:
            update_ncbi(args)


if __name__ == '__main__':
    main()
