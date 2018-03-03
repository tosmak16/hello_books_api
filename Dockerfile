FROM python:3
MAINTAINER Oluwatosin Akinola <tosmak16@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /hellobooks
#VOLUME ["/opt/services/flaskapp/src"]
# We copy the requirements.txt file first to avoid cache invalidations
WORKDIR /hellobooks
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]
