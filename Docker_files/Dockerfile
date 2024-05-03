FROM ubuntu:latest

# Install required packages
RUN apt-get update && \
    apt-get install -y bzip2 wget unzip openjdk-11-jre

# Install AWS CLI
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
&& bash Miniconda3-latest-Linux-x86_64.sh -b -f -p $HOME/miniconda \
&& $HOME/miniconda/bin/conda install -c conda-forge -y awscli \
&& rm Miniconda3-latest-Linux-x86_64.sh

# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
#     unzip awscliv2.zip && \
#     ./aws/install && \
#     rm awscliv2.zip && \
#     rm -rf aws

# Install Docker
RUN apt-get update && \
    apt-get install -y docker.io

# Install Nextflow
RUN curl -fsSL https://get.nextflow.io | bash \
    && mv nextflow /usr/bin/ \
    && nextflow self-update

# Set the working directory
WORKDIR /app

# Define the default command to run when the container starts
CMD ["/bin/bash"]