#!/bin/bash
set -e

# Stunnel Configuration
cat /etc/ssl/certs/server/key.pem /etc/ssl/certs/server/cert.pem > /etc/stunnel/stunnel.pem
/etc/init.d/stunnel4 restart

nginx -g "daemon off;"
