.. _tutorials:

Tutorials
=========

This section contains a variety of tutorials that should help get you started
with the `oggmap` package.

.. _tutorial-getting-started:

Getting started
===============

If you are running `oggmap` for the first time, we recommend to either follow the individual
:ref:`oggmap steps <tutorial-oggmap-steps>`
or getting started with either the :doc:`zebrafish case study <zebrafish_example>` (using OrthoFinder results)
or the :doc:`nematode case study <nematode_example>` (using pre-calculated orthomaps), which both cover all essential steps.

.. image:: img/oggmap_steps.png
   :width: 800px
   :align: center
   :alt: oggmap steps

.. _tutorial-pre-calculated-orthomaps:

Pre-calculated orthomaps
========================

In addition to extract gene age classes from `OrthoFinder <https:https://github.com/davidemms/OrthoFinder>`_ results,
`oggmap` has the functionality to parse and extract gene age classes from pre-calculated orthologous group databases,
like `eggNOG <http://eggnog6.embl.de/#/app/home>`_ or
`plaza <https://bioinformatics.psb.ugent.be/plaza/>`_.

If your query species is part of one of these databases, it might be sufficient to use the gene age classes directly
from them and not start the time consuming step of orthologous group detection with `OrthoFinder <https:https://github.com/davidemms/OrthoFinder>`_
or any other related tool (see benchmark of tools at `Quest for Orthologs <https://orthology.benchmarkservice.org/proxy/>`_).

.. note::
   Since gene age class assignment for any query species relies on taxonomic sampling to cover at best all possible
   species tree nodes from the root (origin of life) up to the query species, the pre-calculated orthologous group databases
   might lack species information for certain tree nodes. Orthologous group detection algorithm do not account for missing species
   and as such will influence the taxonomic completeness score.

.. note::
   To link gene age classes and expression data one should use the same genome annotation version for both,
   the orthologous group detection and the gene expression counting. To use the same genome annotation has the benefit
   not to miss any gene in one or the other and decreases the source of error during gene ID mapping.

.. _tutorial-pre-calculated-orthomaps-eggnog:

eggNOG database version 6.0 orthomaps
-------------------------------------

- includes 1322 species

Extracted orthomaps for all Eukaryota from `eggNOG database version 6.0 <http://eggnog6.embl.de/#/app/home>`_ can be downloaded here:

`eggnog6_eukaryota_orthomaps.tsv.zip <https://zenodo.org/record/8360098/files/eggnog6_eukaryota_orthomaps.tsv.zip>`_

To get an orthomap for e.g. the species *Caenorhabditis elegans* (taxID: 6239):

   ::

       from oggmap import qlin, gtf2t2g, of2orthomap, orthomap2tei, datasets
       import pandas as pd
       eggnog6_eukaryota_orthomaps = pd.read_csv('eggnog6_eukaryota_orthomaps.tsv.zip', delimiter='\t')
       query_lineage = qlin.get_qlin(q='Caenorhabditis elegans')
       query_orthomap = eggnog6_eukaryota_orthomaps[eggnog6_eukaryota_orthomaps['taxID']==query_lineage[1]]
       query_orthomap


.. _tutorial-pre-calculated-orthomaps-plaza:

plaza database version 5.0 orthomaps
------------------------------------

The plaza database offers two different sets of gene family clusters,
either homologous (HOMFAM) or orthologous gene families (ORTHOFAM).

plaza dicots database version 5.0
---------------------------------

- includes 98 species

Extracted orthomaps for all dicots (HOMFAM and ORTHOFAM) from `plaza dicots database version 5.0 <https://bioinformatics.psb.ugent.be/plaza/versions/plaza_v5_dicots/>`_ can be downloaded here:

`plaza_v5_dicots_HOMFAM_orthomaps.tsv.zip <https://zenodo.org/record/8360098/files/plaza_v5_dicots_HOMFAM_orthomaps.tsv.zip>`_

`plaza_v5_dicots_ORTHOFAM_orthomaps.tsv.zip <https://zenodo.org/record/8360098/files/plaza_v5_dicots_ORTHOFAM_orthomaps.tsv.zip>`_

plaza monocots database version 5.0
-----------------------------------

- includes 52 species

Extracted orthomaps for all monocots (HOMFAM and ORTHOFAM) from `plaza monocots database version 5.0 <https://bioinformatics.psb.ugent.be/plaza/versions/plaza_v5_monocots/>`_ can be downloaded here:

`plaza_v5_monocots_HOMFAM_orthomaps.tsv.zip <https://zenodo.org/record/8360098/files/plaza_v5_monocots_HOMFAM_orthomaps.tsv.zip>`_

`plaza_v5_monocots_ORTHOFAM_orthomaps.tsv.zip <https://zenodo.org/record/8360098/files/plaza_v5_monocots_ORTHOFAM_orthomaps.tsv.zip>`_

To get an orthomap for e.g. the species *Arabidopsis thaliana* (taxID: 3702):

   ::

       from oggmap import qlin, gtf2t2g, of2orthomap, orthomap2tei, datasets
       import pandas as pd
       plaza_v5_dicots_HOMFAM_orthomaps = pd.read_csv('plaza_v5_dicots_HOMFAM_orthomaps.tsv.zip', delimiter='\t')
       query_lineage = qlin.get_qlin(q='Arabidopsis thaliana')
       query_orthomap = plaza_v5_dicots_HOMFAM_orthomaps[plaza_v5_dicots_HOMFAM_orthomaps['taxID']==query_lineage[1]]
       query_orthomap


.. _tutorial-oggmap-steps:

oggmap - Steps
================

This section contains the main steps of `oggmap` to extract gene age information for a query species up to linking
the extracted gene age classes and expression data of single-cell data sets.

- :doc:`orthofinder`: This tutorial introduces how to run your own OrthoFinder analysis.
- :doc:`query_lineage`: This tutorial introduces how to get taxonomic information.
- :doc:`get_orthomap`: This tutorial introduces how to extract an orthomap (gene age class) from OrthoFinder results or how to import pre-calculated orthomaps.
- :doc:`geneset_overlap`: This tutorial introduces how to match gene or transcript IDs between an orthomap and scRNA data.
- :doc:`add_tei`: This tutorial introduces how to add a transcriptome evolutionary index (short: TEI) to scRNA data.
- :doc:`evolutionary_indices`: This tutorial introduces how to use other evolutionary indices like nucleotide diversity to calculate TEI.

.. _tutorial-oggmap-downstream-analysis:

oggmap - Downstream analysis
==============================

This section contains different downstream analysis options (Step 5).

- :doc:`plotting`: This tutorial introduces some basic concepts of plotting results.
- :doc:`relative_expression`: This tutorial introduces relative expression per gene age class and its contribution to the global TEI per cell or cell type.
- :doc:`pstrata`: This tutorial introduces partial TEI and its contribution to the global TEI per cell or cell type.

Case studies
============

- :doc:`paul15_example`: Notebook - *Mus musculus* hematopoiesis scRNA data example.
- :doc:`nematode_example`: Notebook - *Caenorhabditis elegans* embryogenesis scRNA data example.
- :doc:`zebrafish_example`: Notebook - *Danio rerio* embryogenesis scRNA data example.
- :doc:`frog_example`: Notebook - *Xenopus tropicalis* embryogenesis scRNA data example.
- :doc:`mouse_example`: Notebook - *Mus musculus* embryogenesis scRNA data example.
- :doc:`hydra_example`: Notebook - *Hydra vulgaris* cell atlas scRNA data example.

.. note::
   A demo dataset is available for each of the tutorial notebooks above.
   These datasets allow you to begin exploring `oggmap` even if you do not have any data at any step in the analysis
   pipeline.

Command line functions
======================

- :doc:`commandline`: This section highlight all `oggmap` functions that can be run via the command line.

myTAI - Function correspondance
===============================

- :doc:`mytai`: This tutorial covers which oggmap functions correspond to myTAI functions.

Prerequisites
=============

- This tutorial assumes that you have basic **Python programming experience**.
  In particular, we assume you are familiar with using a notebook from the following python data science libraries:
  **jupyter**.
- To better understand plotting and data access, the user should try to get familiar with the python libraries:
  **pandas**, **matplotlib** and **seaborn**.
- `oggmap` is a python package but part of it can be run on the command line. For the installation of `oggmap`,
  we recommend using `Anaconda <https://anaconda.org>`_
  (:ref:`see here <install_oggmap>`).
  If you are not familiar with Anaconda or python environment management,
  please use :ref:`our pre-built docker image <docker_image>`.

Code and data availability
==========================

- We provide links for the notebook in each tutorial section.

- You can download the demo input data in the notebooks using the :ref:`module_datasets`.

