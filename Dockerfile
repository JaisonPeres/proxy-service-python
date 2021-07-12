FROM python:3.6-alpine

RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app
ENV WORKERS=2
ENV PORT=8000

EXPOSE $PORT
CMD gunicorn -b :$PORT -w $WORKERS wsgi --log-level debug
