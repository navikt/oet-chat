FROM ghcr.io/navikt/baseimages/python:3.10

USER root
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]