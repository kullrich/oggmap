.. _cmd_qlin:

Command line function - qlin
============================

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