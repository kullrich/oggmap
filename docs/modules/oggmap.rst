.. _module_oggmap:

oggmap - Command line functions
=================================

Command line function - oggmap
--------------------------------

::

    oggmap -h

    options:
      -h, --help            show this help message and exit

    sub-commands:
      {cds2aa,gtf2t2g,ncbitax,of2orthomap,orthomcl2orthomap,plaza2orthomap,qlin}
                            sub-commands help
        cds2aa              translate CDS to AA and optional retain longest isoform <cds2aa -h>
        gtf2t2g             extract transcript to gene table from GTF <gtf2t2g -h>
        ncbitax             update local ncbi taxonomy database <ncbitax -h>
        of2orthomap         extract orthomap from OrthoFinder output for query species <of2orthomap -h>
        orthomcl2orthomap   extract orthomap from orthomcl output for query species <orthomcl2orthomap -h>
        plaza2orthomap      extract orthomap from PLAZA gene family data for query species <of2orthomap -h>
        qlin                get query lineage based on ncbi taxonomy <qlin -h>

Command line function - cds2aa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    oggmap cds2aa -h

    usage: oggmap <sub-command> cds2aa [-h] [-i I] [-o O] [-t T] [-r R]

    options:
      -h, --help  show this help message and exit
      -i I        specify fasta input file
      -o O        specify output file [optional]
      -t T        transtable [default: std]
      -r R        specify CDS source to retain longest isoform

    cds2aa example:

        # to get CDS from Danio rerio on Linux run:
        $ wget https://ftp.ensembl.org/pub/release-105/fasta/danio_rerio/cds/Danio_rerio.GRCz11.cds.all.fa.gz
        $ gunzip Danio_rerio.GRCz11.cds.all.fa.gz

        # on Mac:
        $ curl https://ftp.ensembl.org/pub/release-105/fasta/danio_rerio/cds/Danio_rerio.GRCz11.cds.all.fa.gz --remote-name
        $ gunzip Danio_rerio.GRCz11.cds.all.fa.gz

        # translate and retain longest isoform from CDS fasta file:
        $ cds2aa -i Danio_rerio.GRCz11.cds.all.fa -r ENSEMBL -o Danio_rerio.GRCz11.aa.all.longest.fa

Command line function - gtf2t2g
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    oggmap gtf2t2g -h

    usage: oggmap <sub-command> gtf2t2g [-h] [-i I] [-o O] [-g] [-b] [-p] [-v] [-s] [-q] [-overwrite OVERWRITE]

    options:
      -h, --help            show this help message and exit
      -i I                  specify GTF input file
      -o O                  specify output file [optional]
      -g                    specify if gene names should be appended if they exist
      -b                    specify if gene biotype should be appended if they exist
      -p                    specify if protein id should be appended if they exist
      -v                    specify if gene/transcript/protein version should be appended
      -s                    specify if summary should be printed
      -q                    specify if output should be quite
      -overwrite OVERWRITE  specify if existing output file should be overwritten (default: True)

    gtf2t2g example:

        # to get GTF from Mus musculus on Linux run:
        $ wget https://ftp.ensembl.org/pub/release-108/gtf/mus_musculus/Mus_musculus.GRCm39.108.chr.gtf.gz

        # on Mac:
        $ curl https://ftp.ensembl.org/pub/release-108/gtf/mus_musculus/Mus_musculus.GRCm39.108.chr.gtf.gz --remote-name

        # create t2g from GTF:
        $ gtf2t2g -i Mus_musculus.GRCm39.108.chr.gtf.gz -o Mus_musculus.GRCm39.108.chr.gtf.t2g.tsv -g -b -p -v -s

Command line function - ncbitax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    oggmap ncbitax -h

    usage: oggmap <sub-command> ncbitax [-h] [-u]

    options:
      -h, --help  show this help message and exit
      -u          update

    ncbitax example:

        #update ncbi taxonomy database:
        ncbitax -u

Command line function - of2orthomap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    oggmap of2orthomap -h

    usage: oggmap <sub-command> of2orthomap [-h] [-seqname SEQNAME] [-qt QT] [-sl SL] [-oc OC] [-og OG] [-out OUT] [-overwrite OVERWRITE]

    options:
      -h, --help            show this help message and exit
      -seqname SEQNAME      sequence name of the query species in orthofinder(see column names of <Orthogroups.tsv>)
      -qt QT                query species taxid (e.g. use <oggmap qlin -h> to get taxid)
      -sl SL                species list as <orthofinder name><tab><species taxid> (only samples in this list will be processed)
      -oc OC                specify orthofinder <Orthogroups.GeneCounts.tsv> (see Orthogroups directory)
      -og OG                specify orthofinder <Orthogroups.tsv> (see Orthogroups directory)
      -out OUT              specify output file <orthomap.tsv> (default: orthomap.tsv)
      -overwrite OVERWRITE  specify if existing output file should be overwritten (default: True)

    of2orthomap example:

        # download OrthoFinder example:
        $ wget https://github.com/kullrich/oggmap/raw/main/examples/ensembl_105_orthofinder_Orthogroups.GeneCount.tsv.zip
        $ wget https://github.com/kullrich/oggmap/raw/main/examples/ensembl_105_orthofinder_Orthogroups.tsv.zip
        $ wget https://github.com/kullrich/oggmap/raw/main/examples/ensembl_105_orthofinder_species_list.tsv

        # extract orthomap:
        $ of2orthomap -seqname Danio_rerio.GRCz11.cds.longest -qt 7955 \
          -sl ensembl_105_orthofinder_species_list.tsv \
          -oc ensembl_105_orthofinder_Orthogroups.GeneCount.tsv.zip \
          -og ensembl_105_orthofinder_Orthogroups.tsv.zip

Command line function - qlin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    oggmap qlin -h

    usage: oggmap <sub-command> qlin [-h] [-q Q] [-qt QT]

    options:
      -h, --help  show this help message and exit
      -q Q        query species name
      -qt QT      query species taxid

    qlin example:

        # get query lineage to be used with oggmap later on using query species taxid
        # Mus musculus; 10090
        $ qlin -qt 10090

        # using query species name
        $ qlin -q "Mus musculus"

Modules for dataset downloads
=============================

 .. toctree::

    oggmap.datasets

Modules for eggnog
==================

 .. toctree::

    oggmap.eggnog2orthomap

Modules for GTF handling
========================

 .. toctree::

    oggmap.gtf2t2g

Modules for NCBI taxonomy
=========================

 .. toctree::

    oggmap.ncbitax

Modules for OrthoFinder
=======================

 .. toctree::

    oggmap.of2orthomap

Modules for single-cell data
============================

 .. toctree::

    oggmap.orthomap2tei

Modules for query lineage
=========================

 .. toctree::

    oggmap.qlin
