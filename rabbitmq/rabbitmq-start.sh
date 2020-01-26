#!/bin/bash
set -e

# AMQP Configuration
if [[ -n "${RABBITMQ_USER}" && -n ${RABBITMQ_PASSWORD} ]]; then
  rabbitmq-server -detached
  sleep 6
  rabbitmqctl add_user ${RABBITMQ_USER} ${RABBITMQ_PASSWORD} || echo
  rabbitmqctl set_user_tags ${RABBITMQ_USER} administrator || echo
  #if [ -n "${RABBITMQ_VHOST}" ]; then
  #  rabbitmqctl add_vhost ${RABBITMQ_VHOST} || echo 
  #  rabbitmqctl set_permissions -p ${RABBITMQ_VHOST} ${RABBITMQ_USER} .\* .\* .\* || echo
  #fi
  #rabbitmqctl delete_user guest || echo
  #rabbitmqctl set_permissions -p / guest .\* .\* .\* || echo

  rabbitmqctl stop
  echo "************** Go to sleep"
  sleep 4
  echo "************** Launch rabbit"
fi

ulimit -S -n 65536
rabbitmq-server
