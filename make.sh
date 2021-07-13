rm -rf static
mkdir static

mkdir static/docs
cp -r docs/build/html/* static/docs/

mkdir static/app
cp web-validator/dist/* static/app/

#web-env/bin/gunicorn --bind=0.0.0.0:9000 mementoweb.validator.web.server:app
