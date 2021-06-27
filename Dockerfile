FROM python:3.8

RUN echo '* libraries/restart-without-asking boolean true' | debconf-set-selections
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    nginx libpq-dev libproj-dev libfreetype6-dev libjpeg-dev \
    libxml2-dev libxslt1-dev libffi-dev libssl-dev debconf locales \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/django/app/static

COPY conf /opt/django

RUN rm /etc/nginx/sites-enabled/default \
    && ln -s /opt/django/django.conf /etc/nginx/sites-enabled/

WORKDIR /opt/django/app/

COPY coolsite/requirements.txt /opt/django/requirements.txt
RUN pip3.8 install -r /opt/django/requirements.txt

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

COPY coolsite /opt/django/app
RUN python3.8 /opt/django/app/manage.py collectstatic --noinput

VOLUME ["/opt/django/persistent/media"]

CMD service nginx start && python3.8 /opt/django/app/manage.py migrate --noinput && gunicorn -w 2 --bind=unix:/opt/django/app.sock coolsite.wsgi
