FROM python:3.11.3-bullseye

COPY requirements-for-docker-c.txt /tmp/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements-for-docker-c.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor

RUN mkdir -p /home/dev

# Configure supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]