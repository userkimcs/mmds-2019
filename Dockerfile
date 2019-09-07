FROM ubuntu:18.04

ENV LANG C.UTF-8

# set timezone
RUN apt-get update && apt-get install -y tzdata

RUN apt-get update && \
    apt-get install -y --no-install-recommends tk-dev && \
	apt-get install -y --no-install-recommends apt-utils

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8

# set locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# install python

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install git -y



RUN rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/userkimcs/mmds-2019.git

RUN cd /mmds-2019 && pip3 install -r requirements.txt

WORKDIR /mmds-2019

ENTRYPOINT "bash run.sh"