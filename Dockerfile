FROM google/cloud-sdk
MAINTAINER elliswu<ellis.w@inwinstack.com>

RUN apt-get install python-setuptools
RUN easy_install pip
RUN pip install paho-mqtt
RUN pip install --upgrade google-api-python-client
COPY mqtt_to_bigqery.py /mqtt_to_bq/
COPY mqtt.conf /mqtt_to_bq/
WORKDIR mqtt_to_bq

ENTRYPOINT ["python", "/mqtt_to_bq/mqtt_to_bigqery.py"]