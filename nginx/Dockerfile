FROM bengosney/py-docker-gen

MAINTAINER Ben Gosney <bengosney@googlemail.com>

COPY nginx.tpl /opt/app/

CMD python /opt/app/py-docker-gen.py \
     --filter hostname \
     --notify nginx-proxy \
     /opt/app/nginx.tpl \
     /tmp/conf/proxy.conf
