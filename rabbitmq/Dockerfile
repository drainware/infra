FROM ubuntu:16.04

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux
# Work around initramfs-tools running on kernel 'upgrade': <http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=594189>
ENV INITRD No

WORKDIR /tmp
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y wget

COPY releases/rabbitmq-server_3.0.4-1_all.deb /tmp/rabbitmq-server_3.0.4-1_all.deb
RUN dpkg -i rabbitmq-server_3.0.4-1_all.deb || echo '-'
RUN apt-get -f install -y

#RUN rabbitmq-plugins enable rabbitmq_mqtt rabbitmq_stomp rabbitmq_management rabbitmq_management_agent rabbitmq_management_visualiser rabbitmq_federation rabbitmq_federation_management sockjs
RUN rabbitmq-plugins enable rabbitmq_management rabbitmq_management_agent rabbitmq_management_visualiser rabbitmq_federation rabbitmq_federation_management sockjs

ADD ./rabbitmq-start.sh /root/rabbitmq-start
#ADD ./rabbitmq.config /etc/rabbitmq/rabbitmq.config
RUN chmod +x /root/rabbitmq-start

# AMQP port and Management interface, epmd port, and the inet_dist_listen_min through inet_dist_listen_max ranges
EXPOSE 5672 15672 4369 9100 9101 9102 9103 9104 9105

ENTRYPOINT ["/root/rabbitmq-start"]
