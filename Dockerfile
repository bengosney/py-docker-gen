FROM hypriot/rpi-python

MAINTAINER Ben Gosney <bengosney@googlemail.com>

COPY py-docker-gen.py /opt/app/
COPY requirements.txt /opt/app
RUN pip install -r /opt/app/requirements.txt
