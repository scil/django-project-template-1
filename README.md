# Django 2.0+ project template

This is a simple Django 2.0+ project template with my preferred setup. Most Django project templates make way too many assumptions or are just way too complicated. I try to make the least amount of assumptions possible while still trying provide a useful setup. Most of my projects are deployed to Heroku, so this is optimized for that but is not necessary.

## Features

- Django 2.0+
- Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
- Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
- Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
- HTTPS and other security related settings on Staging and Production.
- Procfile for running gunicorn with New Relic's Python agent.
- PostgreSQL database support with psycopg2.

## Features added by scil

- wsgi server [bjoern](https://github.com/jonashaag/bjoern) or gunicorn ( with systemd conf )
- [direnv](https://github.com/direnv/direnv)
- Django-environ
- add dir project_templates which holds templates used by whole project
- systemd unit file to run pipenv and gunicorn with socket. 
- [Argon2](https://docs.djangoproject.com/en/2.1/topics/auth/passwords/#using-argon2-with-django) to hash the passwords

 .env vars
- DJANGO_DEBUG_TOOLBAR_ENABLE='yes': enable debug-toolbar.   so it's possible to use DJANGO_DEBUG='yes' without debug_toolbar
- DJANGO_USE_I18N='yes' : set USE_I18N=True and add middleware 'django.middleware.locale.LocaleMiddleware'

run gunicorn by pipenv
```bash
sudo /usr/local/bin/pipenv run gunicorn  --access-logfile -  --pid /run/gunicorn_${project_name}/pid   --bind unix:/run/gunicorn_${project_name}/socket   ${project_name}.wsgi:application
curl --unix-socket /run/gunicorn_${project_name}/socket <a url like mysite.test/about/>
```

use systemd
```bash
# nginx conf see: http://docs.gunicorn.org/en/stable/deploy.html#systemd
#
# 1. replace `User=vagrant`  with your user whoes home dir is used by pipenv
sed -i "s/User=vagrant/User=$USER/" conf/systemd/systemd.conf 
# 2. publish systemd unit file
sudo cp -f conf/systemd/systemd.conf /usr/lib/systemd/system/gunicorn.$project_name.service
sudo cp -f conf/systemd/systemd.socket.conf /usr/lib/systemd/system/gunicorn.$project_name.socket
# 3. start 
sudo systemctl enable gunicorn.$project_name
sudo systemctl start gunicorn.$project_name
sudo systemctl status gunicorn.$project_name

```

## How to install

```bash
project_name=<project_name>

# if using mysql
sudo apt-get install libmysqlclient-dev

# if using WSGI Server [bjoern](https://github.com/jonashaag/bjoern) which also requires a C compiler  and Python3 development package
# https://github.com/jonashaag/bjoern/wiki/Installation
sudo apt-get install -y libev-dev

sudo apt-get install -y direnv

sudo pip3 install  pipenv  Django==2.1.7

django-admin.py startproject  --template=https://github.com/scil/django-project-template-1/archive/master.zip \
 --name=example.env  --extension=py,md,html,txt,conf  $project_name  

cd $project_name

mv example.env .env

# edit Pipfile
#   remove psycopg2 or mysqlclient if PostgreSQL or MySql is not needed
#   remove bjoern or gunicorn, left one server
#   use url= "https://pypi.douban.com/simple"  if in China
vi Pipfile

LDFLAGS=-L/usr/local/lib CFLAGS=-I/usr/local/include pipenv install --dev

# use corret  path to your virtualenvs
echo . /home/vagrant/.local/share/virtualenvs/${project_name}-<...>/bin/activate > .envrc
direnv allow

pipenv run python manage.py collectstatic
```

## Environment variables

These are common between environments. The `ENVIRONMENT` variable loads the correct settings, possible values are: `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT='DEVELOPMENT'
DJANGO_SECRET_KEY='dont-tell-eve'
DJANGO_DEBUG='yes'
```

These settings(and their default values) are only used on staging and production environments.

```
DJANGO_SESSION_COOKIE_SECURE='yes'
DJANGO_SECURE_BROWSER_XSS_FILTER='yes'
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF='yes'
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='yes'
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_REDIRECT_EXEMPT=''
DJANGO_SECURE_SSL_HOST=''
DJANGO_SECURE_SSL_REDIRECT='yes'
DJANGO_SECURE_PROXY_SSL_HEADER='HTTP_X_FORWARDED_PROTO,https'
```

## Deployment

It is possible to deploy to Heroku or to your own server.

## License

The MIT License (MIT)

Copyright (c) 2012-2017 José Padilla

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
