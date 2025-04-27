FROM python:3.9-alpine

RUN apk add --no-cache python3

ADD requirements.pip requirements.pip
RUN pip install -r requirements.pip

ADD src src

EXPOSE 5000

CMD ["python3", "/src/run.py"]
