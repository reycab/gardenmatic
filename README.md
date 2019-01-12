# GARDENMATIC

Django: 2.0

## Development tools


### Editorconfig

Use common rules for formatting code

http://editorconfig.org

### Virtual Env

```
virtualenv venv -p python3

```

### Djang-env

https://github.com/jpadilla/django-dotenv

Create a `.env` or cp `cp .env.example .env` file with the below content:

```bash

DJANGO_SETTINGS_MODULE="config.settings.dev"
SECRET_KEY=""
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DOMAIN=""
DOMAIN_URL=""
STATIC_URL="/static/"
MEDIA_URL="/media/"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 2525
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ""
```
