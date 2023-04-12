ARG PYTHON_VERSION=3.11.2
ARG ALPINE_VERSION=3.17

FROM python:${PYTHON_VERSION}-slim-buster AS poetry

# Configure Poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.4.0

RUN mkdir -p ${POETRY_HOME}

RUN apt-get update \
    && apt-get --no-install-recommends install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/install-poetry.py \
    | python3 - --version ${POETRY_VERSION} --yes

ENV PATH=${POETRY_HOME}/bin:${PATH}

WORKDIR /lazykh

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true \
    && poetry install

# open shell
CMD ["/bin/bash"]

# FROM ubuntu:18.04 as base

# RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# # Full list of packages (including GPU specific ones):
# RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
#     --mount=target=/var/cache/apt,type=cache,sharing=locked \
#     apt-get update && \
#     apt-get install -y --no-install-recommends \
#     autoconf \
#     automake \
#     bzip2 \
#     ca-certificates \
#     ffmpeg \
#     g++ \
#     gcc \
#     gfortran \
#     git \
#     libatlas3-base \
#     libc++-dev \
#     libstdc++-6-dev \
#     libtool \
#     make \
#     nvidia-cuda-dev \
#     patch \
#     python \
#     python-dev \
#     python-pip \
#     python3 \
#     python3-dev \
#     python3-pip \
#     sox \
#     subversion \
#     unzip \
#     vim \
#     wget \
#     zlib1g-dev

# WORKDIR /lazykh


# COPY gentle/ext gentle/ext

# RUN cd /gentle/ext && \
#     ./install_kaldi.sh && \
#     make depend && make -j $(nproc) && rm -rf kaldi *.o

FROM debian:10-slim as kaldi

ENV DIR_LAZYKH=/lazykh
ENV DIR_GENTLE=/lazykh/third_party/gentle
ENV DIR_KALDI=${DIR_GENTLE}/ext/kaldi
ENV DIR_KALDI_TOOLS=${DIR_KALDI}/tools
ENV DIR_KALDI_SRC=${DIR_KALDI}/src

RUN apt-get update -qq && \
    apt-get install -qq --no-install-recommends \
    g++ \
    make \
    automake \
    autoconf \
    bzip2 \
    unzip \
    wget \
    sox \
    libtool \
    git \
    subversion \
    python2.7 \
    python3 \
    zlib1g-dev \
    ca-certificates \
    gfortran \
    patch \
    ffmpeg \
    vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${DIR_LAZYKH}

COPY . .

RUN cd $DIR_GENTLE && \
    git submodule update --init --recursive

# 01. Creates a symbolic link to python3 as python (required by Kaldi)
# 02. Installs the mandatory Kaldi tools 
# 03. Installs the OpenBLAS library (required by Gentle) Note: The script
#     install_openblas.sh will prompt the user, so we use the yes command to
#     answer yes to all the prompts
# 04. Configures Kaldi
# 05. Installs the Gentle models
# 06. Compiles Gentle (Kaldi and Gentle are compiled in a single step)
# 07. Removes the Kaldi and Gentle built files and artifacts
# 08. Removes the Kaldi and Gentle git directories Note: All the steps are done
#     in a single RUN command to avoid creating intermediate layers, which would
#     increase the image size
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    cd ${DIR_KALDI_TOOLS} && \
    make -j $(nproc) -w -s && \
    MAKEFLAGS="-j $(nproc) -w -s" \
    ./extras/install_openblas.sh && \
    cd ${DIR_KALDI_SRC} && \
    ./configure --static --static-math=yes --static-fst=yes --use-cuda=no --openblas-root=${DIR_KALDI_TOOLS}/OpenBLAS/install && \
    cd ${DIR_GENTLE} && \
    yes | ./install_models.sh && \
    cd ${DIR_GENTLE}/ext && \
    make -j depend && \
    make -j $(nproc) -w -s && \
    find ${DIR_KALDI} -type f \( -name "*.o" -o -name "*.la" -o -name "*.a" \) -exec rm {} \; && \
    find ${DIR_GENTLE}/ext -type f \( -name "*.o" -o -name "*.la" -o -name "*.a" \) -exec rm {} \; && \
    rm -rf ${DIR_GENTLE}/.git && \
    rm -rf ${DIR_KALDI}/.git

FROM python:3.9-slim-buster as gentle

COPY lazykh

# bla bla bla

CMD [uvicorn]
# and gentle