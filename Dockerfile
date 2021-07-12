FROM python:3.6 AS compile-image
ARG API_URL
ENV API_URL=${API_URL}
ARG API_AUTH_PATH
ENV API_AUTH_PATH=${API_AUTH_PATH}
RUN mkdir /app && pip install pipenv==2018.11.26
WORKDIR /app
ENV PIPENV_VENV_IN_PROJECT=1
ADD . /app
RUN pipenv install --skip-lock

FROM python:3.6 AS dev
COPY --from=compile-image /app /app
WORKDIR /app
ENV PORT=8000
EXPOSE $PORT
ENV PATH=/app/.venv/bin:$PATH
CMD python api.py


FROM python:3.6 AS prod
COPY --from=compile-image /app /app
WORKDIR /app
ENV WORKERS=2
ENV PORT=8000
ENV LOG_LEVEL=info
ENV PATH=/app/.venv/bin:$PATH
EXPOSE $PORT
CMD gunicorn -b :$PORT --log-level ${LOG_LEVEL}  -w $WORKERS wsgi
