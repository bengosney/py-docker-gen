FROM hypriot/rpi-python

MAINTAINER Ben Gosney <bengosney@googlemail.com>

RUN mkdir -p /opt/app/
COPY requirements.txt /opt/app
RUN pip install -r /opt/app/requirements.txt

COPY py-docker-gen.py /opt/app/

RUN mkdir -p /etc/nginx/conf.d
COPY nginx.tpl /opt/app/nginx.tpl

CMD python /opt/app/py-docker-gen.py \
     --filter hostname \
     nginx.tpl \
     /etc/nginx/conf.d/proxy.conf
