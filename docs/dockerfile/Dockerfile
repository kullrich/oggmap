FROM ubuntu:24.04

LABEL version="0.0.2"
LABEL description="oggmap docker installation"
LABEL maintainer="ullrich@evolbio.mpg.de"

RUN apt-get update && apt-get install -y adduser \
 && useradd docker \
 && mkdir /home/docker \
 && chown docker:docker /home/docker \
 && adduser docker staff
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 ed \
 less \
 locales \
 vim-tiny \
 wget \
 ca-certificates \
 fonts-texgyre \
 && rm -rf /var/lib/apt/lists/*
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen en_US.utf8 \
 && /usr/sbin/update-locale LANG=en_US.UTF-8 \
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 libcurl4-openssl-dev \
 libssl-dev \
 libxml2-dev \
 libglu1-mesa-dev \
 libgit2-dev \
 pandoc \
 libssh2-1-dev \
 libfontconfig1-dev \
 libharfbuzz-dev \
 libfribidi-dev \
 libfreetype6-dev \
 libpng-dev \
 libtiff5-dev \
 libjpeg-dev \
 libpython3-dev \
 python3-dev \
 python3-pip \
 python3-venv \
 gcc \
 g++ \
 libz-dev \
 git
# Clone oggmap
RUN cd /home/docker \
 && git clone https://github.com/kullrich/oggmap.git
# Install miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
 && bash miniconda.sh -b -p /home/docker/miniconda \
 && rm miniconda.sh
# Configure miniconda and install packages
RUN . "/home/docker/miniconda/etc/profile.d/conda.sh" \
 && cd \
 && hash -r \
 && export PATH="/home/docker/miniconda/bin:${PATH}" \
 && conda config --set always_yes yes --set changeps1 no \
 && conda activate \
 && conda install -c conda-forge mamba \
 && cd /home/docker/oggmap \
 && mamba env create -q --file environment.yml \
 && conda activate oggmap_env \
 && pip install . --default-timeout=100 \
 && ncbitax -u \
 && pytest \
 && pip install jupyter \
 && pip install ipykernel \
 && python -m ipykernel install --user --name=oggmap_env \
 && cd /home/docker \
 && rm -r oggmap \
 && conda clean --all \
 && conda init bash \
 && echo "conda activate oggmap_env" >> $HOME/.bashrc