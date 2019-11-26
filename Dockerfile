FROM ubuntu:16.04

MAINTAINER Daniele ARIOLI <d.arioli@studenti.unipi.it>

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-setuptools python3-pip git

ADD . /code
WORKDIR code

RUN python3 -m pip install -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

EXPOSE 5000

CMD ["python3","email_digest.py"]
