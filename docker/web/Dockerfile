FROM python:3.11
# sudo apt-get install libtidy-dev
RUN apt-get update && apt-get install -y \
    libtidy-dev \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ../.. /code/
