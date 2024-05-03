# Use a base image with Java and other dependencies
FROM ubuntu:latest

# Install necessary tools (wget, unzip) and clean up the package manager cache
RUN apt-get update && \
    apt-get install -y curl unzip openjdk-11-jdk tabix && \
    rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

WORKDIR /app

# Download and install SnpEff
RUN curl "https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip" -o "snpeff_latest_core.zip" && \
    unzip snpeff_latest_core.zip && \
    rm snpeff_latest_core.zip && \
    java -jar ./snpEff/snpEff.jar download -v hg38

WORKDIR /app/snpEff

# Set environment variables for SnpEff
ENV SNPEFF_HOME /app/snpEff
ENV PATH $SNPEFF_HOME:$PATH
