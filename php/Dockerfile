FROM php:5.6-fpm
RUN apt-get update && apt-get install -y \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libmcrypt-dev \
        libpng-dev \
    && docker-php-ext-install -j$(nproc) iconv mcrypt \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd

RUN apt-get install libssl-dev libcurl4-openssl-dev pkg-config -y
RUN apt-get install python-pip libssl-dev monit -y

RUN pecl install mongo \
    && docker-php-ext-enable mongo

RUN pip install pika==0.9.5 pymongo==3.6.1 pyopenssl MultipartPostHandler

RUN mkdir -p /var/lib/php/session
RUN chmod -R 777 /var/lib/php/session

RUN mkdir -p /opt/drainware/

COPY ./monit/monitrc /etc/monit/monitrc
RUN chmod 0700 /etc/monit/monitrc

COPY ./php.ini /usr/local/etc/php/

COPY ./entrypoint.sh /entrypoint.sh
