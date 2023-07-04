ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

# Set DATABASE_URL for building purposes
ENV DATABASE_URL "sqlite://:memory:"
# Set SECRET_KEY for building purposes
ENV SECRET_KEY "O4WX51fjyVPOUWOmFNg25zK2UE0BE3gtlro7EJTbt2IW0xy9Op"
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "web_project.wsgi"]
