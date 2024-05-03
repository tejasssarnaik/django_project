FROM python:3.9.12-slim-buster

RUN pip install -U cython poetry

# Update packages and install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl unzip git procps && \
    apt-get clean

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm awscliv2.zip

RUN git clone https://github.com/pwwang/vcfstats.git

WORKDIR /vcfstats

RUN poetry config virtualenvs.create false && \
    pip install -U pip && \
    poetry update && \
    poetry install

# Start the container with a shell
CMD ["/bin/bash"]