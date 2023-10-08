FROM python:3.10.7
SHELL ["/bin/bash", "-c"]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /star-burger/requirements.txt
WORKDIR /star-burger
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
