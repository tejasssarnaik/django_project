# Use the miniconda base image
FROM continuumio/miniconda3:latest

# Install MULTIQC and AWS cli
RUN apt-get update && \
    apt-get install -y curl unzip && \
    pip install --upgrade --force-reinstall git+https://github.com/ewels/MultiQC.git

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install


# Set working directory
WORKDIR /app

# Start the container with a shell
CMD ["/bin/bash"]
