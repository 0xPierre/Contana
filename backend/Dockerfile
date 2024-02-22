###########
# BUILDER #
###########
FROM python:3.11-slim as builder

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install "setuptools<58.0.0"
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /app/requirements.txt

FROM python:3.11-slim

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

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install "setuptools<58.0.0"
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

COPY . /app

RUN adduser --system --group django_user && chown -R django_user:django_user /app
#    && chown -R django_user:django_user /usr/local/lib/python3.7/site-packages/guardian/

USER django_user
