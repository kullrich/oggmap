.. _singularity_additional_information:

oggmap singularity quick start and additional notes
=====================================================

In this documentation, we provide example commands for our oggmap docker image to be used with singularity below. But we are not aiming to provide detailed information about general singularity usage on docker images.
We highly recommend learning about docker and singularity if you are not familiar with it, and make sure you have adequate knowledge about docker and singularity prior to start oggmap analysis with singularity.

Quick start - Singularity - bash
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Download oggmap docker image from docker Hub.

::

    singularity pull docker://kkuweb/oggmap_ubuntu:latest

2. Start running it.

- To access files smoothly, we can use `bind paths and mounts <https://docs.sylabs.io/guides/3.0/user-guide/bind_paths_and_mounts.html>`_. Here, we will mount the `data_folder`, a directory in your local machine.

::

    mkdir data_folder # Create data folder in your local environment.
    singularity shell \
      --bind $(pwd)/data_folder:/mnt/data_folder \
      oggmap_ubuntu_latest.sif

3. Activate conda environment oggmap_env.

::

    source /home/docker/miniconda/etc/profile.d/conda.sh
    conda activate oggmap_env

4. Start using oggmap bash scripts.

::

    cd /mnt/data_folder
    oggmap -h
    oggmap qlin -q "Arabidopsis thaliana"

Docker image build information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We built our docker image using Dockerfile automatic build function.
The Dockerfile is available `here <https://github.com/kullrich/oggmap/blob/main/docs/dockerfile>`_.
You can modify it to create custom docker image by yourself.
If you make custom environment, please do so on your responsibility.
