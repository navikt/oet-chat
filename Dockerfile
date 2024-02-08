FROM ghcr.io/navikt/baseimages/python:3.8

USER root
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]