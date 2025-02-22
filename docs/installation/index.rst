.. _installation:

Installation
============

Please follow the guide below to install oggmap and its dependent software.

.. _require:

If a containerised option is available to you (docker or singularity) it will help you to either
isolate it from the host environment or deals with the situation of broken conde dependencies (with only limited control
on our side to resolve these issues). We of course try to support conda and other issues,
but if you want to avoid conda issues, the suggestion is to use either docker or singularity.

.. _docker_image:

Docker image
------------

Pre-built docker image is available through `Docker Hub <https://hub.docker.com/repository/docker/kkuweb/oggmap_ubuntu>`_ .
::

    docker pull kkuweb/oggmap_ubuntu:latest

- This docker image was built based on Ubuntu 22.04.

- Python dependent packages and oggmap are installed in an anaconda environment, `oggmap_env`. This environment will be activated automatically when you log in.

- See additional information

.. toctree::
   :maxdepth: 1

   docker_additional_information

.. _singularity_image:

Singularity image
-----------------

- Pre-built docker image is available through `Docker Hub <https://hub.docker.com/repository/docker/kkuweb/oggmap_ubuntu>`_ .

::

    singularity pull docker://kkuweb/oggmap_ubuntu:latest

- This docker image was built based on Ubuntu 22.04.
- Python dependent packages and oggmap are installed in an anaconda environment, `oggmap_env`. This environment needs to be activated when you log in.
- See additional information

.. toctree::
   :maxdepth: 1

   singularity_additional_information

.. _install_oggmap:

Install oggmap
----------------

Python Requirements
^^^^^^^^^^^^^^^^^^^

- oggmap v0.0.1 was developed using Python `3.8`. We do not support Python `2.7x` or Python `<=3.7`.
- oggmap v0.0.2 was developed using Python `3.10`. We do not support Python `2.7x` or Python `<=3.10`.

oggmap installation using conda and pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  We recommend installing oggmap in an independent conda environment to avoid dependent software conflicts.
  Please make a new python environment for oggmap and install dependent libraries in it.

  The environment is created with `conda create` in which oggmap is installed.

  If you do not have a working installation of Python `3.10` (or later), consider
  installing `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_. Then run:

  ::

      git clone https://github.com/kullrich/oggmap.git
      cd oggmap
      conda env create --file environment.yml
      conda activate oggmap_env

  Install `oggmap` via `PyPI <https://pypi.org/project/oggmap>`_:

  ::

      pip install oggmap

Development Version
^^^^^^^^^^^^^^^^^^^

To work with the latest version `on GitHub <https://github.com/kullrich/oggmap>`_: clone the repository and `cd` into its root directory.

  ::

      git clone kullrich/oggmap
      cd oggmap

Install `oggmap` into your current python environment:

  ::

      pip install .

Installing Miniconda
^^^^^^^^^^^^^^^^^^^^

After downloading `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, in a unix shell (Linux, Mac), run

  ::

      cd DOWNLOAD_DIR
      chmod +x Miniconda3-latest-VERSION.sh
      ./Miniconda3-latest-VERSION.sh

