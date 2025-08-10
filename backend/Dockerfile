###########
# BUILDER #
###########
FROM python:3.13-slim as builder

ENV PYTHON_VERSION=3.13

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=2.0.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache
ENV POETRY_CACHE_DIR=/opt/.cache
# Poetry uses VIRTUAL_ENV to determine whether it is running in a virtual environment
ENV VIRTUAL_ENV=/opt/venv

# Create stage for Poetry installation
FROM builder AS poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM poetry-base AS compile-image

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Create a virtual environment for the application
RUN python3 -m venv ${VIRTUAL_ENV}

# Activate the virtual environment
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Don't try to write .pyc files on the import of source modules
ENV PYTHONDONTWRITEBYTECODE 1
# Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml README.md ./

RUN poetry check
RUN rm -rf $(poetry config cache-dir)/artifacts
RUN poetry install --no-interaction --no-cache


FROM compile-image

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installation of wkhtmltopdf
RUN apt-get update --fix-missing
RUN apt-get install -y fontconfig libfreetype6 libjpeg62-turbo libpng16-16 \
    libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base libfontconfig1 \
    fontconfig-config libx11-data libxau6 libxdmcp6 xfonts-utils ucf fonts-dejavu-core \
    ttf-bitstream-vera fonts-liberation libbsd0 libfontenc1 libxfont2 \
    x11-common xfonts-encodings
RUN apt-get install -y wkhtmltopdf

RUN apt-get install -y postgresql-client

WORKDIR /app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
COPY --from=compile-image ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app
RUN adduser --disabled-password --no-create-home django_user  \
    && chown -R django_user:django_user /app
 USER django_user
