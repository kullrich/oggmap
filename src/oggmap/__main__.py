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
from Bio import SeqIO
from oggmap import broccoli2orthomap, cds2aa, eggnog2orthomap, gtf2t2g, ncbitax, of2orthomap, orthomcl2orthomap, plaza2orthomap, qlin


def define_parser():
    """
    A helper function for using `oggmap` via the terminal.

    :return: An argparse.ArgumentParser.

    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='oggmap',
                                     usage='%(prog)s <sub-command>',
                                     description='oggmap')
    subparsers = parser.add_subparsers(dest='subcommand',
                                       title='sub-commands',
                                       help='sub-commands help')
    cds2aa_example = '''cds2aa example:

    # to get CDS from Danio rerio on Linux run:
    $ wget https://ftp.ensembl.org/pub/release-113/fasta/danio_rerio/cds/Danio_rerio.GRCz11.cds.all.fa.gz
    $ gunzip Danio_rerio.GRCz11.cds.all.fa.gz

    # on Mac:
    $ curl https://ftp.ensembl.org/pub/release-113/fasta/danio_rerio/cds/Danio_rerio.GRCz11.cds.all.fa.gz --remote-name
    $ gunzip Danio_rerio.GRCz11.cds.all.fa.gz
    
    # translate and retain longest isoform from CDS fasta file:
    $ cds2aa -i Danio_rerio.GRCz11.cds.all.fa -r ENSEMBL -o Danio_rerio.GRCz11.aa.all.longest.fa
    
    # translate and retain longest isoform from CDS fasta file and shorten in case not multiple of three:
    $ cds2aa -i Danio_rerio.GRCz11.cds.all.fa -r ENSEMBL -o Danio_rerio.GRCz11.aa.all.longest.fa -s
    '''
    eggnog2orthomap_example = '''eggnog2orthomap example:

    # download EggNOG v6.0 data:
    $ wget http://eggnog6.embl.de/download/eggnog_6.0/e6.og2seqs_and_species.tsv

    # extract orthomap:
    $ eggnog2orthomap -qt 10090 \\
      -og e6.og2seqs_and_species.tsv \\
      -dbname taxadb.sqlite
    '''
    gtf2t2g_example = '''gtf2t2g example:

    # to get GTF from Mus musculus on Linux run:
    $ wget https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Mus_musculus.GRCm39.113.chr.gtf.gz

    # on Mac:
    $ curl https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Mus_musculus.GRCm39.113.chr.gtf.gz --remote-name

    # create t2g from GTF:
    $ gtf2t2g -i Mus_musculus.GRCm39.113.chr.gtf.gz -o Mus_musculus.GRCm39.113.chr.gtf.t2g.tsv -g -b -p -v -s
    '''
    ncbitax_example = '''ncbitax example:

    #update ncbi taxonomy database:
    ncbitax -u -outdir taxadb -t taxa -dbname taxadb.sqlite
    '''
    of2orthomap_example = '''of2orthomap example:

    # download OrthoFinder example:
    $ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_Orthogroups.GeneCount.tsv.zip
    $ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_Orthogroups.tsv.zip
    $ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_species_list.tsv
    
    # extract orthomap:
    $ of2orthomap -seqname 7955.danio_rerio.pep -qt 7955 \\
      -sl ensembl_113_orthofinder_last_species_list.tsv \\
      -oc ensembl_113_orthofinder_last_Orthogroups.GeneCount.tsv.zip \\
      -og ensembl_113_orthofinder_last_Orthogroups.tsv.zip \\
      -dbname taxadb.sqlite
    '''
    orthomcl2orthomap_example = '''orthomcl2orthomap example:

    # download OrthoMCL DB data:
    $ wget https://beta.orthomcl.org/common/downloads/release-6.21/genomeSummary_OrthoMCL-6.21.txt.gz
    $ gunzip genomeSummary_OrthoMCL-6.21.txt.gz
    $ wget https://beta.orthomcl.org/common/downloads/release-6.21/groups_OrthoMCL-6.21.txt.gz
    $ gunzip groups_OrthoMCL-6.21.txt.gz

    # quickly find 'Arabidopsis thaliana' short name
    # grep 'Arabidopsis thaliana' genomeSummary_OrthoMCL-6.21.txt
    
    # extract orthomap:
    $ orthomcl2orthomap -tla atha \\
      -sl genomeSummary_OrthoMCL-6.21.txt \\
      -og groups_OrthoMCL-6.21.txt \\
      -out atha.orthomap \\
      -dbname taxadb.sqlite
    '''
    plaza2orthomap_example = '''plaza2orthomap example:
    
    # download Species information and Gene Family Clusters from Dicots PLAZA 5.0 data:
    $ wget https://ftp.psb.ugent.be/pub/plaza/plaza_public_dicots_05/SpeciesInformation/species_information.csv.gz
    $ gunzip species_information.csv.gz
    $ wget https://ftp.psb.ugent.be/pub/plaza/plaza_public_dicots_05/GeneFamilies/genefamily_data.ORTHOFAM.csv.gz
    $ gunzip genefamily_data.ORTHOFAM.csv.gz
    $ wget https://ftp.psb.ugent.be/pub/plaza/plaza_public_dicots_05/GeneFamilies/genefamily_data.HOMFAM.csv.gz
    $ gunzip  genefamily_data.HOMFAM.csv.gz
    
    # using Orthologous gene family 
    $ plaza2orthomap -qt 3702 \\
      -sl species_information.csv \\
      -og genefamily_data.ORTHOFAM.csv \\
      -out 3702.orthofam.orthomap \\
      -dbname taxadb.sqlite
    
    # using Homologous gene family 
    $ plaza2orthomap -qt 3702 \\
      -sl species_information.csv \\
      -og genefamily_data.HOMFAM.csv \\
      -out 3702.homfam.orthomap \\
      -dbname taxadb.sqlite
    '''
    qlin_example = '''qlin example:

    # get query lineage to be used with oggmap later on using query species taxID
    # Mus musculus; 10090
    $ qlin -qt 10090 \\
      -dbname taxadb.sqlite

    # using query species name
    $ qlin -q "Mus musculus" \\
      -dbname taxadb.sqlite
    '''
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
    broccoli2orthomap_parser = subparsers.add_parser(name='broccoli2orthomap',
                                                     help='extract orthomap from Broccoli data for query species '
                                                          '<broccoli2orthomap -h>',
                                                     epilog=broccoli2orthomap_example,
                                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    cds2aa_parser = subparsers.add_parser(name='cds2aa',
                                          help='translate CDS to AA and optional retain longest isoform <cds2aa -h>',
                                          epilog=cds2aa_example,
                                          formatter_class=argparse.RawDescriptionHelpFormatter)
    eggnog2orthomap_parser = subparsers.add_parser(name='eggnog2orthomap',
                                                  help='extract orthomap from eggnog output for query species '
                                                       '<eggnog2orthomap -h>',
                                                  epilog=eggnog2orthomap_example,
                                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    gtf2t2g_parser = subparsers.add_parser(name='gtf2t2g',
                                           help='extract transcript to gene table from GTF <gtf2t2g -h>',
                                           epilog=gtf2t2g_example,
                                           formatter_class=argparse.RawDescriptionHelpFormatter)
    ncbitax_parser = subparsers.add_parser(name='ncbitax',
                                           help='update local ncbi taxonomy database <ncbitax -h>',
                                           epilog=ncbitax_example,
                                           formatter_class=argparse.RawDescriptionHelpFormatter)
    of2orthomap_parser = subparsers.add_parser(name='of2orthomap',
                                               help='extract orthomap from OrthoFinder output for query species '
                                                    '<of2orthomap -h>',
                                               epilog=of2orthomap_example,
                                               formatter_class=argparse.RawDescriptionHelpFormatter)
    orthomcl2orthomap_parser = subparsers.add_parser(name='orthomcl2orthomap',
                                               help='extract orthomap from orthomcl output for query species '
                                                    '<orthomcl2orthomap -h>',
                                               epilog=orthomcl2orthomap_example,
                                               formatter_class=argparse.RawDescriptionHelpFormatter)
    plaza2orthomap_parser = subparsers.add_parser(name='plaza2orthomap',
                                                  help='extract orthomap from PLAZA gene family data for query species '
                                                       '<plaza2orthomap -h>',
                                                  epilog=plaza2orthomap_example,
                                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    qlin_parser = subparsers.add_parser(name='qlin',
                                        help='get query lineage based on ncbi taxonomy <qlin -h>',
                                        epilog=qlin_example,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    broccoli2orthomap.add_argparse_args(parser=broccoli2orthomap_parser)
    cds2aa.add_argparse_args(parser=cds2aa_parser)
    eggnog2orthomap.add_argparse_args(parser=eggnog2orthomap_parser)
    gtf2t2g.add_argparse_args(parser=gtf2t2g_parser)
    ncbitax.add_argparse_args(parser=ncbitax_parser)
    of2orthomap.add_argparse_args(parser=of2orthomap_parser)
    orthomcl2orthomap.add_argparse_args(parser=orthomcl2orthomap_parser)
    plaza2orthomap.add_argparse_args(parser=plaza2orthomap_parser)
    qlin.add_argparse_args(parser=qlin_parser)
    return parser


def main():
    """
    The main function that is being called when `oggmap` is used via the terminal.
    """
    parser = define_parser()
    args: argparse.Namespace = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
        sys.exit()
    if args.subcommand == 'broccoli2orthomap':
        print(args)
        if not args.dbname:
            print('\nError <-dbname>: Please specify taxadb.sqlite file')
            sys.exit()
        if not args.seqname:
            parser.print_help()
            print('\nError <-seqname>: Please specify query species name in Broccoli and taxid')
            sys.exit()
        if not args.qt:
            parser.print_help()
            print('\nError <-qt>: Please specify query species taxid')
            sys.exit()
        if not args.sl:
            parser.print_help()
            print('\nError <-sl>: Please specify species list as <Broccoli name><tab><species taxid>')
            sys.exit()
        if not args.oc:
            parser.print_help()
            print('\nError <-oc>: Please specify Broccoli <table_OGs_protein_counts.txt> (see dir_step3 directory)')
            sys.exit()
        if not args.og:
            parser.print_help()
            print('\nError <-og>: Please specify Broccoli <table_OGs_protein_names.txt> (see dir_step3 directory)')
            sys.exit()
        of2orthomap.get_orthomap(seqname=args.seqname,
                                 qt=args.qt,
                                 sl=args.sl,
                                 oc=args.oc,
                                 og=args.og,
                                 out=args.out,
                                 quiet=False,
                                 continuity=True,
                                 overwrite=args.overwrite,
                                 dbname=args.dbname)
    if args.subcommand == 'cds2aa':
        if args.o is None:
            sys.stderr.write(str(args))
        else:
            print(args)
        if args.i is None and sys.stdin.isatty():
            parser.print_help()
            sys.exit('\nPlease provide STDIN or input file')
        if args.i is None and not sys.stdin.isatty():
            record_iter = SeqIO.parse(sys.stdin,
                                      "fasta")
        else:
            record_iter = SeqIO.parse(args.i,
                                      "fasta")
        if args.r:
            record_gene_len_dict = cds2aa.get_gene_len_dict(record_iter,
                                                            args.r)
            record_iter = iter([x[1] for x in record_gene_len_dict.values()])
        cds2aa_iter = cds2aa.cds2aa_record(record_iter,
                                           cds2aa.transtable[args.t])
        if args.o is None:
            SeqIO.write(cds2aa_iter,
                        sys.stdout,
                        "fasta")
        else:
            count = SeqIO.write(cds2aa_iter,
                                args.o,
                                "fasta")
            print("translated %i sequences" % count)
    if args.subcommand == 'eggnog2orthomap':
        print(args)
        if not args.dbname:
            print('\nError <-dbname>: Please specify taxadb.sqlite file')
            sys.exit()
        if not args.qt:
            parser.print_help()
            print('\nError <-qt>: Please specify query species taxID')
            sys.exit()
        if not args.og:
            parser.print_help()
            print('\nError <-og>: Please specify eggnog <e6.og2seqs_and_species.tsv>')
            sys.exit()
        eggnog2orthomap.get_eggnog_orthomap(args.qt,
                                            args.og,
                                            subset=args.subset,
                                            out=args.out,
                                            overwrite=args.overwrite,
                                            dbname=args.dbname)
    if args.subcommand == 'gtf2t2g':
        print(args)
        if not args.i:
            parser.print_help()
            print('\nError <-i>: Please specify GTF input file')
            sys.exit()
        if args.o:
            if os.path.exists(args.o) and not args.overwrite:
                print('\nError <-overwrite>: output file exists, please set to True if it should be overwritten\n')
                sys.exit()
            output = open(args.o,
                          'w')
        else:
            output = sys.stdout
        gtf2t2g.parse_gtf(gtf=args.i,
                          g=args.g,
                          b=args.b,
                          p=args.p,
                          v=args.v,
                          s=args.s,
                          output=output,
                          q=args.q)
        output.close()
    if args.subcommand == 'ncbitax':
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
                ncbitax.update_ncbi(args)
    if args.subcommand == 'of2orthomap':
        print(args)
        if not args.dbname:
            print('\nError <-dbname>: Please specify taxadb.sqlite file')
            sys.exit()
        if not args.seqname:
            parser.print_help()
            print('\nError <-seqname>: Please specify query species name in OrthoFinder and taxid')
            sys.exit()
        if not args.qt:
            parser.print_help()
            print('\nError <-qt>: Please specify query species taxid')
            sys.exit()
        if not args.sl:
            parser.print_help()
            print('\nError <-sl>: Please specify species list as <OrthoFinder name><tab><species taxid>')
            sys.exit()
        if not args.oc:
            parser.print_help()
            print('\nError <-oc>: Please specify OrthoFinder <Orthogroups.GeneCounts.tsv> (see Orthogroups directory)')
            sys.exit()
        if not args.og:
            parser.print_help()
            print('\nError <-og>: Please specify OrthoFinder <Orthogroups.tsv> (see Orthogroups directory)')
            sys.exit()
        of2orthomap.get_orthomap(seqname=args.seqname,
                                 qt=args.qt,
                                 sl=args.sl,
                                 oc=args.oc,
                                 og=args.og,
                                 out=args.out,
                                 quiet=False,
                                 continuity=True,
                                 overwrite=args.overwrite,
                                 dbname=args.dbname)
    if args.subcommand == 'orthomcl2orthomap':
        print(args)
        if not args.dbname:
            print('\nError <-dbname>: Please specify taxadb.sqlite file')
            sys.exit()
        if not args.tla:
            parser.print_help()
            print('\nError <-tla>: Please specify query species OrthoMCL short name (THREE_LETTER_ABBREV)')
            sys.exit()
        if not args.sl:
            parser.print_help()
            print('\nError <-sl>: Please specify OrthoMCL species information file <genomeSummary_OrthoMCL-6.16.txt>')
            sys.exit()
        if not args.og:
            parser.print_help()
            print('\nError <-og>: Please specify OrthoMCL groups file <groups_OrthoMCL-6.16.txt>')
            sys.exit()
        orthomcl2orthomap.get_orthomcl_orthomap(tla=args.tla,
                                                sl=args.sl,
                                                og=args.og,
                                                out=args.out,
                                                quiet=False,
                                                continuity=True,
                                                overwrite=args.overwrite,
                                                dbname=args.dbname)
    if args.subcommand == 'plaza2orthomap':
        print(args)
        if not args.dbname:
            print('\nError <-dbname>: Please specify taxadb.sqlite file')
            sys.exit()
        if not args.qt:
            parser.print_help()
            print('\nError <-qt>: Please specify query species taxID')
            sys.exit()
        if not args.sl:
            parser.print_help()
            print('\nError <-sl>: Please specify PLAZA species information file <species_information.csv>')
            sys.exit()
        if not args.og:
            parser.print_help()
            print('\nError <-og>: Please specify PLAZA gene family file <genefamily_data.ORTHOFAM.csv> or '
                  '<genefamily_data.HOMFAM.csv>')
            sys.exit()
        plaza2orthomap.get_plaza_orthomap(qt=args.qt,
                                          sl=args.sl,
                                          og=args.og,
                                          out=args.out,
                                          quiet=False,
                                          continuity=True,
                                          overwrite=args.overwrite,
                                          dbname=args.dbname)
    if args.subcommand == 'qlin':
        print(args)
        if not args.dbname:
            print('\nError <-dbname> : Please specify taxadb.sqlite file')
            sys.exit()
        if not args.q and not args.qt:
            parser.print_help()
            print('\nError <-q> <-qt>: Please specify query species name or taxid')
            sys.exit()
        if args.q and args.qt:
            parser.print_help()
            print('\nWarning: Since both query species name and taxid are given taxid is used')
            sys.exit()
        qlin.get_qlin(q=args.q,
                      qt=args.qt,
                      quiet=False,
                      dbname=args.dbname)


if __name__ == '__main__':
    main()
