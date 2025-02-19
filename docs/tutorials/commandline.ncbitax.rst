.. _cmd_ncbitax:

Command line function - ncbitax
===============================

::

    oggmap ncbitax -h

    usage: oggmap <sub-command> ncbitax [-h] [-u] [-outdir OUTDIR] [-t T] [-dbname DBNAME] [-chunk CHUNK] [-force] [-verbose]

    options:
       -h, --help      show this help message and exit
       -u              update
       -outdir OUTDIR  output directory option for taxadb2 download
       -t T            type option for taxadb2 download (default: taxa)
       -dbname DBNAME  dbname option for taxadb2 create (default: taxadb.sqlite)
       -chunk CHUNK    chunk option for taxadb2 create (default: 500)
       -force          force option for taxadb2 download (default: False)
       -verbose        increase verbosity (default: False)

    ncbitax example:

        #update ncbi taxonomy database:
        ncbitax -u -outdir taxadb -type taxa -dbname taxadb.sqlite