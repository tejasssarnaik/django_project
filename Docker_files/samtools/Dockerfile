# Use the Ubuntu base image
FROM ubuntu:latest

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl unzip samtools && \
    apt-get clean

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip

# Set the working directory
WORKDIR /app

# Start the container with a shell
CMD ["/bin/bash"]