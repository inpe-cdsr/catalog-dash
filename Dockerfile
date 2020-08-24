FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update -y \
    && apt-get install -y gcc libmariadb-dev\
    && rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
#     apt-get install -qqy software-properties-common --no-install-recommends && \
#     apt-get update && \
#     apt-get install -y python-gdal python3-gdal gdal-bin

RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=America/Sao_Paulo

EXPOSE 8050

CMD [ "python", "main.py" ]
