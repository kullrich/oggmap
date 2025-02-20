.. _cmd_orthomcl2orthomap:

Command line function - orthomcl2orthomap
=========================================

::

    oggmap orthomcl2orthomap -h

    usage: oggmap <sub-command> orthomcl2orthomap [-h] [-tla TLA] [-sl SL] [-og OG] [-out OUT] [-overwrite OVERWRITE] [-dbname DBNAME]

    options:
      -h, --help            show this help message and exit
      -tla TLA              query species orthomcl short name (THREE_LETTER_ABBREV)
      -sl SL                specify orthomcl species information file <genomeSummary_OrthoMCL-6.16.txt>
      -og OG                specify orthomcl groups file <groups_OrthoMCL-6.16.txt>
      -out OUT              specify output file <orthomap.tsv> (default: orthomap.tsv)
      -overwrite OVERWRITE  specify if existing output file should be overwritten (default: True)
      -dbname DBNAME        taxadb.sqlite file

    orthomcl2orthomap example:

        # download OrthoMCL DB data:
        $ wget https://beta.orthomcl.org/common/downloads/release-6.21/genomeSummary_OrthoMCL-6.21.txt.gz
        $ gunzip genomeSummary_OrthoMCL-6.21.txt.gz
        $ wget https://beta.orthomcl.org/common/downloads/release-6.21/groups_OrthoMCL-6.21.txt.gz
        $ gunzip groups_OrthoMCL-6.21.txt.gz

        # quickly find 'Arabidopsis thaliana' short name
        # grep 'Arabidopsis thaliana' genomeSummary_OrthoMCL-6.21.txt

        # extract orthomap:
        $ orthomcl2orthomap -tla atha \
          -sl genomeSummary_OrthoMCL-6.21.txt \
          -og groups_OrthoMCL-6.21.txt \
          -out atha.orthomap \
          -dbname taxadb.sqlite