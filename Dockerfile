FROM python:3.10-alpine

ENV PATH="/scripts:${PATH}"

# Installing dependencies
COPY ./requirements.txt /requirements.txt
# Installing dependencies to install uwsgi
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

# Copying the django project into the container
RUN mkdir /app
COPY ./csgo_compare /app
WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

# Making folders for static and media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media

# Moving exmaple media files
COPY ./csgo_compare/media/ /vol/web/media

# Adding new user so site not running as root
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]