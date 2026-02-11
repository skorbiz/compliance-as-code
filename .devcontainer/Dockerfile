# FROM mcr.microsoft.com/.devcontainer/mezcada_defaults/base:jammy
FROM ubuntu:24.04

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y --no-install-recommends \
    bash-completion \
    python3 \
    python3-pip \
    python3.12-venv \
    python3.12-dev \
    software-properties-common \
    curl \
    wget \
    xz-utils \
    sudo \
    git

# Install UV 0.9.21 for python package management
RUN curl -LsSf https://astral.sh/uv/0.9.21/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

# Install Typst for document compilation
RUN wget -qO /tmp/typst.tar.xz https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz && \
    tar xf /tmp/typst.tar.xz --strip-components=1 -C /usr/local/bin typst-x86_64-unknown-linux-musl/typst && \
    rm /tmp/typst.tar.xz && \
    typst --version

# ruff==0.14.10
# pyrefly==0.46.2


# Set users
# Ubuntu 24.04 adding a default user named ubuntu with gid and uid 1000
# Rename the ubuntu user to dev, move the home directory, and change the group. Obs this assumes uid and gid 1000.
# https://askubuntu.com/questions/1513927/ubuntu-24-04-docker-images-now-includes-user-ubuntu-with-uid-gid-1000
# https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-rename-linux-users-and-their-home-directory/
RUN usermod -l dev ubuntu   
RUN usermod -d /home/dev -m dev
RUN groupmod -n dev ubuntu

RUN echo 'dev:Docker!' | chpasswd
RUN echo 'root:Docker!' | chpasswd
RUN usermod --append --groups systemd-journal dev
WORKDIR /home/dev


# Cleanup
RUN rm -rf /root/.cache/pip/*. \
    && rm -rf /var/lib/apt/lists/*
