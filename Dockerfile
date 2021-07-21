LABEL   maintainer="Bhanuka Mahanama <bhanuka@lanl.gov>"

FROM node:14.15.5
WORKDIR ./
RUN sh make-static.sh
COPY static ./staic

FROM    python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD     ["gunicorn", "--bind=0.0.0.0:9000", "mementoweb.validator.web.server:app"]

