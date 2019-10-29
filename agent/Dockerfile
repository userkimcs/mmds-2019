FROM ubuntu:18.10


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && apt-get install git -y

RUN git clone https://github.com/userkimcs/mmds-2019.git

WORKDIR /mmds-2019

# start with entrypoint
# --entrypoint=script.sh
#ENTRYPOINT bash $start_script
