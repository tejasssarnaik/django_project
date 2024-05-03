# Use a base image with Java installed
FROM openjdk:8

# Set the working directory
WORKDIR /app

# Install wget
RUN apt-get update && apt-get install -y wget curl

# Download Qualimap
RUN wget https://bitbucket.org/kokonech/qualimap/downloads/qualimap_v2.2.1.zip && \
    unzip qualimap_v2.2.1.zip && \
    rm qualimap_v2.2.1.zip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip

# Add Qualimap to the PATH
ENV PATH="/app/qualimap_v2.2.1/:${PATH}"

# Set the default command to run when the container is launched
CMD ["/bin/bash"]