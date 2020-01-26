FROM debian:8

RUN apt-get update 
RUN apt-get install -y python-pip libssl-dev
RUN pip install pika==0.9.6 pyopenssl

COPY entrypoint.sh /entrypoint.sh
COPY endpoint.py /tmp/endpoint.py
RUN chmod +x /entrypoint.sh

