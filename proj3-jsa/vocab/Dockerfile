FROM python:3.5.2
MAINTAINER Brian Veber "bveber@uoregon.edu"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_vocab.py"]
