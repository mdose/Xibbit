FROM ubuntu:latest
MAINTAINER Megan Dose "megan.e.dose@gmail.com"
RUN apt update -y
RUN apt install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]
