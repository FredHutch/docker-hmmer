FROM ubuntu:16.04
MAINTAINER sminot@fredhutch.org

# Install prerequisites
RUN apt update && \
    apt-get install -y wget curl unzip python3 python3-pip bats \
    awscli libcurl4-openssl-dev hmmer

# Add the wrapper scripts to the PATH
ADD . /usr/local/hmmer_scripts/
RUN ln -s /usr/local/hmmer_scripts/hmmbuild.py /usr/local/bin/
RUN ln -s /usr/local/hmmer_scripts/hmmsearch.py /usr/local/bin/

# Add to the Python PATH
ENV PYTHONPATH "${PYTONPATH}:/usr/local/hmmer_scripts"

# Run tests
ADD tests/ /usr/local/tests
RUN bats /usr/local/tests && \
    rm -r /usr/local/tests
