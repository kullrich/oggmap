# oggmap

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/kullrich/oggmap/build_check.yml?branch=main)](https://github.com/kullrich/oggmap/actions/workflows/build_check.yml)
[![PyPI](https://img.shields.io/pypi/v/oggmap?color=blue)](https://pypi.org/project/oggmap/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oggmap)](https://pypi.org/project/oggmap/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/oggmap)](https://pypi.org/project/oggmap/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![docs-badge](https://readthedocs.org/projects/oggmap/badge/?version=latest)](https://oggmap.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://img.shields.io/badge/DOI-10.1093/bioinformatics/btad657-blue)](https://doi.org/10.1093/bioinformatics/btad657)

## orthologous maps - evolutionary age index

[`oggmap`](https://github.com/kullrich/oggmap) is a python package to extract orthologous maps
(short: `orthomap` or in other words the evolutionary age of a given orthologous group) from OrthoFinder or eggNOG results.
Oggmap results (gene ages per orthologous group) can be further used to calculate and visualize weighted expression data
(transcriptome evolutionary index) from scRNA sequencing objects.

![oggmap steps](docs/tutorials/img/oggmap_steps.png)
![zebrafish example](docs/tutorials/img/zebrafish_tei.png)
![nematode example](docs/tutorials/img/nematode_pi.png)

## Documentation

Online documentation can be found [here](https://oggmap.readthedocs.io/en/latest/).

When using `oggmap` in published research, please cite:

- Ullrich KK, Glytnasi NE, "oggmap: a Python package to extract gene ages per orthogroup and link them with single-cell RNA data", Bioinformatics, 2023, 39(11). [https://doi.org/10.1093/bioinformatics/btad657](https://doi.org/10.1093/bioinformatics/btad657)

## Installing `oggmap`

More installation options can be found [here](https://oggmap.readthedocs.io/en/latest/installation/index.html).

### oggmap installation using conda and pip

We recommend installing `oggmap` in an independent conda environment to avoid dependent software conflicts.
Please make a new python environment for `oggmap` and install dependent libraries in it.

If you do not have a working installation of Python 3.10 (or later),
consider installing [Anaconda](https://docs.anaconda.com/anaconda/install/) or
[Miniconda](https://docs.conda.io/en/latest/miniconda.html).

To create and activate the environment run:

```shell
$ git clone https://github.com/kullrich/oggmap.git
$ cd oggmap
$ conda env create --file environment.yml
$ conda activate oggmap_env
```

Then to install `oggmap` via PyPI:

```shell
$ pip install oggmap
```

## Quick usage

Detailed tutorials how to use `oggmap` can be found [here](https://oggmap.readthedocs.io/en/latest/tutorials/index.html).

### Update/download local ncbi taxonomic database:

The following command downloads or updates your local copy of the
NCBI's taxonomy database (~150MB). The database is saved at `-dbname`
set to default `taxadb.sqlite`.

```shell
$ oggmap ncbitax -u -outdir taxadb -type taxa -dbname taxadb.sqlite
$ rm -rf taxadb
```

```python
>>> from oggmap import ncbitax
>>> update_parser = ncbitax.define_parser()
>>> update_args = update_parser.parse_args()
>>> update_args.outdir = 'taxadb'
>>> update_args.dbname = 'taxadb.sqlite'
>>> ncbitax.update_ncbi(update_args)
```

### Step 1 - Get query species taxonomic lineage information:

You can query a species lineage information based on its name or its
taxID. For example `Danio rerio` with taxID `7955`:

```shell
$ oggmap qlin -q "Danio rerio" -dbname taxadb.sqlite
$ oggmap qlin -qt 7955 -dbname taxadb.sqlite
```

```python
>>> from oggmap import qlin
>>> qlin.get_qlin(q='Danio rerio',
...     dbname = 'taxadb.sqlite')
>>> qlin.get_qlin(qt='7955',
...     dbname = 'taxadb.sqlite')
```

You can get the query species topology as a tree.
For example for `Danio rerio` with taxID `7955`:

```python
>>> from io import StringIO
>>> from Bio import Phylo
>>> from oggmap import qlin
>>> query_topology = qlin.get_lineage_topo(qt='7955',
...     dbname='taxadb.sqlite')
>>> output = StringIO()
>>> Phylo.write(query_topology, output, "newick")
>>> output.getvalue().strip()
```

### Step 2 - Get query species orthomap from OrthoFinder results:

The following code extracts the `orthomap` for `Danio rerio` based on pre-calculated 
OrthoFinder results and ensembl release-113:

OrthoFinder results (-S diamond_ultra_sens) using translated, longest-isoform coding sequences
from ensembl release-113 have been archived and can be found
[here](https://zenodo.org/record/7242264#.Y1p19i0Rowc).

```shell
# download OrthoFinder example:
$ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_Orthogroups.GeneCount.tsv.zip
$ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_Orthogroups.tsv.zip
$ wget https://zenodo.org/records/14680521/files/ensembl_113_orthofinder_last_species_list.tsv    

# extract orthomap:
$ oggmap of2orthomap -seqname 7955.danio_rerio.pep -qt 7955 \\
  -sl ensembl_113_orthofinder_last_species_list.tsv \\
  -oc ensembl_113_orthofinder_last_Orthogroups.GeneCount.tsv.zip \\
  -og ensembl_113_orthofinder_last_Orthogroups.tsv.zip \\
  -dbname taxadb.sqlite
```

```python
>>> from oggmap import datasets, of2orthomap, qlin
>>> datasets.ensembl113_last(datapath='.')
>>> query_orthomap, orthofinder_species_list, of_species_abundance = of2orthomap.get_orthomap(
...     seqname='7955.danio_rerio.pep',
...     qt='7955',
...     sl='ensembl_113_orthofinder_last_species_list.tsv',
...     oc='ensembl_113_orthofinder_last_Orthogroups.GeneCount.tsv.zip',
...     og='ensembl_113_orthofinder_last_Orthogroups.tsv.zip',
...     out=None,
...     quiet=False,
...     continuity=True,
...     overwrite=True,
...     dbname='taxadb.sqlite')
>>> query_orthomap
```

### Step 3 - Map OrthoFinder gene names and scRNA gene/transcript names:

The following code extracts the gene to transcript table for `Danio rerio`:

GTF file obtained from [here](https://ftp.ensembl.org/pub/release-105/gtf/danio_rerio/Danio_rerio.GRCz11.105.gtf.gz).

```shell
# to get GTF from Mus musculus on Linux run:
$ wget https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Mus_musculus.GRCm39.113.chr.gtf.gz
# on Mac:
$ curl https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Mus_musculus.GRCm39.113.chr.gtf.gz --remote-name

# create t2g from GTF:
$ oggmap gtf2t2g -i Mus_musculus.GRCm39.113.chr.gtf.gz \\
  -o Mus_musculus.GRCm39.113.chr.gtf.t2g.tsv \\
  -g -b -p -v -s
```

```python
>>> from oggmap import datasets, gtf2t2g
>>> gtf_file = datasets.zebrafish_ensembl113_gtf(datapath='.')
>>> query_species_t2g = gtf2t2g.parse_gtf(
...     gtf=gtf_file,
...     g=True, b=True, p=True, v=True, s=True, q=True)
>>> query_species_t2g
```

Import now, the scRNA dataset of the query species.

example: **Danio rerio** - [http://tome.gs.washington.edu](http://tome.gs.washington.edu)
([Qui et al. 2022](https://www.nature.com/articles/s41588-022-01018-x))

`AnnData` file can be found [here](https://doi.org/10.5281/zenodo.7243602).

```python
>>> import scanpy as sc
>>> from oggmap import datasets, orthomap2tei
>>> # download zebrafish scRNA data here: https://doi.org/10.5281/zenodo.7243602
>>> # or download with datasets.qiu22_zebrafish(datapath='.')
>>> zebrafish_data = datasets.qiu22_zebrafish(datapath='.')
>>> zebrafish_data
>>> # check overlap of transcript table <gene_id> and scRNA data <var_names>
>>> orthomap2tei.geneset_overlap(zebrafish_data.var_names, query_species_t2g['gene_id'])
```

The `replace_by` helper function can be used to add a new column to the `orthomap` dataframe by matching e.g.
gene isoform names and their corresponding gene names.

```python
>>> # convert orthomap transcript IDs into GeneIDs and add them to orthomap
>>> query_orthomap['geneID'] = orthomap2tei.replace_by(
...    x_orig = query_orthomap['seqID'],
...    xmatch = query_species_t2g['transcript_id_version'],
...    xreplace = query_species_t2g['gene_id'])
>>> # check overlap of orthomap <geneID> and scRNA data
>>> orthomap2tei.geneset_overlap(zebrafish_data.var_names, query_orthomap['geneID'])
```

### Step 4 - Get transcriptome evolutionary index (TEI) values and add them to scRNA dataset:

Since now the gene names correspond to each other in the `orthomap` and the scRNA adata object,
one can calculate the transcriptome evolutionary index (TEI) and add them to the scRNA dataset (adata object).

```python
>>> # add TEI values to existing adata object
>>> orthomap2tei.get_tei(adata = zebrafish_data,
...    gene_id = query_orthomap['geneID'],
...    gene_age = query_orthomap['PSnum'],
...    keep = 'min',
...    layer = None,
...    add = True,
...    obs_name = 'tei',
...    boot = False,
...    bt = 10,
...    normalize_total = False,
...    log1p = False,
...    target_sum = 1e6)
```

### Step 5 - Downstream analysis

Once the gene age data has been added to the scRNA dataset,
one can e.g. plot the corresponding transcriptome evolutionary index (TEI) values
by any given observation pre-defined in the scRNA dataset.

#### Boxplot TEI per stage:

```python
>>>sc.pl.violin(adata = zebrafish_data,
...     keys = ['tei'],
...     groupby = 'stage',
...     rotation = 90,
...     palette = 'Paired',
...     stripplot = False,
...     inner = 'box')
```

## oggmap via Command Line

`oggmap` can also be used via the command line.

Command line documentation can be found [here](https://oggmap.readthedocs.io/en/latest/modules/oggmap.html).

```shell
$ oggmap -h
```

```
usage: oggmap <sub-command>

oggmap

options:
  -h, --help            show this help message and exit

sub-commands:
  {cds2aa,gtf2t2g,ncbitax,of2orthomap,orthomcl2orthomap,plaza2orthomap,qlin}
                        sub-commands help
    cds2aa              translate CDS to AA and optional retain longest
                        isoform <cds2aa -h>
    gtf2t2g             extract transcript to gene table from GTF
                        <gtf2t2g -h>
    ncbitax             update local ncbi taxonomy database <ncbitax -h>
    of2orthomap         extract orthomap from OrthoFinder output for
                        query species <of2orthomap -h>
    orthomcl2orthomap   extract orthomap from orthomcl output for
                        query species <orthomcl2orthomap -h>
    plaza2orthomap      extract orthomap from PLAZA gene family data
                        for query species <of2orthomap -h>
    qlin                get query lineage based on ncbi taxonomy <qlin -h>
```

To retrieve e.g. the lineage information for `Danio rerio` run the following command:

```shell
$ oggmap qlin -q "Danio rerio" -dbname taxadb.sqlite
```

## Development Version

To work with the latest version [on GitHub](https://github.com/kullrich/oggmap):
clone the repository and `cd` into its root directory.

```shell
$ git clone kullrich/oggmap
$ cd oggmap
```

Install `oggmap` into your current python environment:

```shell
$ pip install -e .
```

## Testing `oggmap`

`oggmap` has an extensive test suite which is run each time a new contribution
is made to the repository. To run the test suite locally run:

```shell
$ pytest tests
```

## Contributing Code

If you would like to contribute to `oggmap`, please file an issue so that one can establish a statement of need, avoid redundant work, and track progress on your contribution.

Before you do a pull request, you should always file an issue and make sure that someone from the `oggmap` developer team agrees that it's a problem, and is happy with your basic proposal for fixing it.

Once an issue has been filed and we've identified how to best orient your
contribution with package development as a whole,
[fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)
the [main repo](https://github.com/kullrich/oggmap/oggmap.git), branch off a
[feature
branch](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-branches)
from `main`,
[commit](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/committing-and-reviewing-changes-to-your-project)
and
[push](https://docs.github.com/en/github/using-git/pushing-commits-to-a-remote-repository)
your changes to your fork and submit a [pull
request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)
for `oggmap:main`.

By contributing to this project, you agree to abide by the Code of Conduct terms.

## Bug reports

Please post troubles or questions on the GitHub repository [issue tracker](https://github.com/kullrich/oggmap/issues).
Also, please look at the closed issue pages. This might give an answer to your question.

## Inquiry for collaboration or discussion

Please send e-mail to us if you want a discussion with us.

Principal code developer: Kristian Ullrich

E-mail address can be found [here](https://www.evolbio.mpg.de).

## Code of Conduct - Participation guidelines

This repository adheres to the [Contributor Covenant](http://contributor-covenant.org) code of conduct for in any interactions you have within this project. (see [Code of Conduct](https://github.com/kullrich/oggmap/-/blob/master/CODE_OF_CONDUCT.md))

See also the policy against sexualized discrimination, harassment and violence for the Max Planck Society [Code-of-Conduct](https://www.mpg.de/11961177/code-of-conduct-en.pdf).

By contributing to this project, you agree to abide by its terms.

## References

see references [here](https://oggmap.readthedocs.io/en/latest/references/index.html)
