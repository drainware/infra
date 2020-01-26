FROM mongo:3.7.1


COPY ./drainware  /opt/drainware/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD /entrypoint.sh