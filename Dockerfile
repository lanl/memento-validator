FROM node:14.15.5 as node
COPY . .
WORKDIR ./web-validator

RUN rm -rf static
RUN mkdir ../static

RUN rm -rf dist/
RUN npm run build
RUN mkdir ../static/app
RUN cp -r dist/* ../static/app/


FROM    python:3.9
COPY . .
COPY --from=node ../static ./static
WORKDIR .
RUN pip install -r requirements.txt

RUN sphinx-apidoc -o docs/source mementoweb/
RUN sphinx-build docs/source docs/build/html -b html
RUN mkdir static/docs
RUN cp -r docs/build/html/* static/docs/

RUN pip install gunicorn

CMD ["gunicorn", "--bind=0.0.0.0:9000", "mementoweb.validator.web.server:app"]

