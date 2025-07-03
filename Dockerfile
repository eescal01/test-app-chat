# -----------------------------------------------------------------------------
# 🐳 Dockerfile for building an AWS Lambda Layer (Python 3.10, Amazon Linux 2)
# This image is designed for compatibility with AWS Lambda’s runtime and builds
# all dependencies using Poetry in a reproducible environment.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# 🔹 BASE IMAGE
# Uses Amazon Linux 2 to match AWS Lambda runtime environment (x86_64).
# -----------------------------------------------------------------------------
FROM amazonlinux:2

# -----------------------------------------------------------------------------
# 🔖 METADATA LABELS (OCI Standard)
# These labels improve traceability, documentation, and CI/CD introspection.
# -----------------------------------------------------------------------------
LABEL maintainer="Evert Escalante <eescal01>"
LABEL description="Dockerfile for building a compatible AWS Lambda Layer (Amazon Linux 2, Python 3.10, Poetry 2.x)"
LABEL version="1.0.0"
LABEL org.opencontainers.image.authors="Evert Escalante"
LABEL org.opencontainers.image.source="https://github.com/your-org/lambda-layer-build"
LABEL org.opencontainers.image.licenses="Proprietary"

# -----------------------------------------------------------------------------
# ⚙️ INSTALL CORE DEVELOPMENT TOOLS
# Includes compilers and libraries required to build Python packages.
# -----------------------------------------------------------------------------
RUN yum groupinstall "Development Tools" -y && \
    yum install -y \
        gcc \
        openssl11 \
        openssl11-devel \
        libffi-devel \
        bzip2-devel \
        wget \
        curl \
        git \
        zip

# -----------------------------------------------------------------------------
# 🐍 INSTALL PYTHON 3.10 FROM SOURCE
# Ensures exact version matching and compatibility with Poetry environment.
# -----------------------------------------------------------------------------
RUN wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz && \
    tar xzf Python-3.10.2.tgz && \
    cd Python-3.10.2 && \
    ./configure --enable-optimizations && \
    make -j "$(nproc)" && \
    make altinstall && \
    ln -sf /usr/local/bin/python3.10 /usr/bin/python  # Symlink to use `python`

# -----------------------------------------------------------------------------
# 📦 INSTALL POETRY PACKAGE MANAGER
# Poetry is used to manage project dependencies in a clean, lockfile-based way.
# -----------------------------------------------------------------------------
RUN curl -sSL https://install.python-poetry.org | python3.10 -

# Add Poetry to PATH and explicitly define the Python interpreter
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_PYTHON=python3.10

# -----------------------------------------------------------------------------
# 📁 SETUP WORKING DIRECTORY
# Standard build directory used by Makefile or docker-compose pipelines.
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# 📤 COPY PROJECT FILES
# This includes the pyproject.toml and source code required for dependency build.
# -----------------------------------------------------------------------------
COPY . .

# -----------------------------------------------------------------------------
# 🔌 INSTALL DEPENDENCIES WITH POETRY
# Uses plugin 'poetry-plugin-export' for exporting requirements if needed.
# `--no-root` skips installing the local project package.
# -----------------------------------------------------------------------------
RUN poetry self add poetry-plugin-export && \
    poetry install --no-root

# -----------------------------------------------------------------------------
# 🛑 NO CMD DEFINED
# This image is intended to be used as a build step or in automation.
# Use `docker run` with custom entrypoints or `make docker-compose-all`.
# -----------------------------------------------------------------------------
