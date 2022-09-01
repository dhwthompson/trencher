ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    pipenv

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pipenv install --system --deploy

COPY . .

RUN SECRET_KEY="dummy" \
    TODOIST_ACCESS_TOKEN="dummy" \
    TODOIST_PROJECT_ID="0" \
    python manage.py collectstatic --noinput

CMD ["gunicorn", "-c", "conf.py", "--reload", "trencher.wsgi"]
