FROM python:3

COPY /src /root 

WORKDIR /root

RUN pip install fastapi uvicorn torch numpy unidecode

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}