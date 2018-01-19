FROM alpine:latest

MAINTAINER Megan Dose "megan.e.dose@gmail.com"

RUN apk add --no-cache python2 python2-dev py2-pip build-base postgresql-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["server.py"]
