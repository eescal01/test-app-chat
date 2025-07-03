# -----------------------------------------------------------------------------
# Dockerfile for building an AWS Lambda Layer (Python 3.10, Amazon Linux 2)
# Includes recommended maintainer and metadata labels for traceability.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# BASE IMAGE: Amazon Linux 2
# Ensures binary compatibility with AWS Lambda runtime (x86_64).
# -----------------------------------------------------------------------------
FROM amazonlinux:2

# -----------------------------------------------------------------------------
# Recommended metadata labels (maintainer, description, version, etc.)
# Improves traceability, searchability, and compliance with OCI best practices.
# -----------------------------------------------------------------------------
LABEL maintainer="Emmanuel Palacio Gaviria <sixtandev@gmail.com>"
LABEL description="Dockerfile for building a compatible AWS Lambda Layer (Amazon Linux 2, Python 3.10, Poetry 2.x, plugin-export)"
LABEL version="1.0.0"
LABEL org.opencontainers.image.authors="Emmanuel Palacio Gaviria"
LABEL org.opencontainers.image.source="https://github.com/your-org/lambda-layer-kuma-client"
LABEL org.opencontainers.image.licenses="Proprietary"

# -----------------------------------------------------------------------------
# Install core development tools and required system libraries
# -----------------------------------------------------------------------------
RUN yum groupinstall "Development Tools" -y && \
    yum install gcc openssl11 openssl11-devel libffi-devel bzip2-devel wget curl git zip -y

# Instalación de Python 3.10
RUN wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz && \
    tar xzf Python-3.10.2.tgz && \
    cd Python-3.10.2 && \
    ./configure --enable-optimizations && \
    make -j $(nproc) && \
    make altinstall && \
    ln -sf /usr/local/bin/python3.10 /usr/bin/python  # 👈 FIX

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3.10 -

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_PYTHON=python3.10

# -----------------------------------------------------------------------------
# Set working directory for reproducible builds
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# Copy source code and configuration files into the container
# -----------------------------------------------------------------------------
COPY . .

# -----------------------------------------------------------------------------
# Install project dependencies using Poetry (without installing the project root package)
# Add poetry-plugin-export to enable 'poetry export'
# -----------------------------------------------------------------------------
RUN poetry self add poetry-plugin-export
RUN poetry install --no-root

# -----------------------------------------------------------------------------
# (CMD not defined; this container is intended for automated build tasks)
# -----------------------------------------------------------------------------