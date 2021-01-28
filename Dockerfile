FROM alpine:3.10

LABEL Maintainer="Fazil Saleem <fazilsaleem@gmail.com>"

RUN apk update \
&& apk add --no-cache python3 python3-dev py3-pip py3-setuptools libffi-dev gcc   build-base  py-mysqlclient nginx supervisor openssl-dev jpeg-dev pango fontconfig bash ttf-opensans libevent libevent-dev libxml2-dev libxslt-dev mariadb-dev\ 
&& pip3 install wheel \
&& pip3 install cython \
&& apk add --virtual packstodel \
&& adduser -S -G www-data -h /var/www/ www-data \
&& ln -sf /dev/stdout /var/log/nginx/access.log \
&& ln -sf /dev/stderr /var/log/nginx/error.log

ENV LIBRARY_PATH=/lib:/usr/lib
ENV TZ Asia/Kuwait

ADD app/requirements.txt /var/www/

RUN pip3 --no-cache-dir install -r /var/www/requirements.txt \
&& apk del packstodel
RUN chown -R www-data.www-data /var/lib/nginx
ADD docker-deps/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker-deps/nginx/teacher_directory.conf /etc/nginx/conf.d/default.conf
ADD docker-deps/supervisord.ini /etc/supervisor.d/supervisord.ini

ADD app /var/www/
WORKDIR /var/www/

ADD docker-deps/startup.sh /opt/startup.sh


RUN chown -R www-data:www-data /var/tmp/ \
&& chmod 755 /opt/startup.sh

EXPOSE 80 8000

ENTRYPOINT ["/opt/startup.sh"]