# Use a base image with Java and other dependencies
FROM ubuntu:latest

# Install necessary tools (wget, unzip) and clean up the package manager cache
RUN apt-get update && \
    apt-get install -y curl unzip vcfanno tabix && \
    rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

WORKDIR /opt

COPY clinvar_sig.lua /opt/clinvar_sig.lua
COPY conf.toml /opt/conf.toml