# Use the Ubuntu base image
FROM ubuntu:latest

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 curl wget unzip openjdk-11-jdk samtools && \
    wget https://github.com/broadinstitute/gatk/releases/download/4.3.0.0/gatk-4.3.0.0.zip && \
    unzip gatk-4.3.0.0.zip -d /opt/ && \
    ln -s /bin/python3 /usr/bin/python && \
    rm gatk-4.3.0.0.zip && \
    apt-get clean

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

ENV PATH="/opt/gatk-4.3.0.0/:${PATH}"

# Set the working directory
WORKDIR /app

# Start the container with a shell
CMD ["/bin/bash"]