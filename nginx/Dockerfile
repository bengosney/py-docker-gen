FROM bengosney/py-docker-gen-rpi

MAINTAINER Ben Gosney <bengosney@googlemail.com>

RUN mkdir -p /opt/app
RUN mkdir -p /etc/nginx/conf.d

COPY nginx.tpl /opt/app/nginx.tpl

CMD python /opt/app/py-docker-gen.py \
     --filter hostname \
     --notify nginx-proxy \
     nginx.tpl \
     /etc/nginx/conf.d/proxy.conf
