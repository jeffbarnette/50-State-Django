# Pull official base image
FROM python:3.9.1-alpine

# Create directory for the app user
RUN mkdir -p /home/app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV APP_STATIC=/home/app/web/static
RUN mkdir $APP_HOME
RUN mkdir $APP_STATIC

# Set work directory
WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . $APP_HOME

# Install psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev postgresql-dev

# Install dependencies
RUN pip install --upgrade pip pipenv && pipenv install --system --dev

# Create the app user
RUN addgroup -S app && adduser -S app -G app

# Set permissions on all the files to the app user
RUN chown -R app:app $APP_HOME

# Switch to the app user
USER app

# Lint
RUN flake8 .

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]