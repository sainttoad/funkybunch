from python:3

ADD app/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ADD secrets/secrets /secrets

ADD app /funkybunch
WORKDIR /funkybunch

CMD ./funkybunch.py