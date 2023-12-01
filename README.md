
# vscubing api

RESTful api for vscubing.com powerd with Django Rest Framework


## Tech Stack

**Client:** Django, DRF

**Server:** WSGI

**Deploy:** Nginx


## api docs
Check api documentation in [API Docs](docs/README.md) 
## Authors

- [@HomaDev](https://github.com/HomaDev)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file


`SECRET_KEY` = 'django-key'

`DEBUG` = 1 # 1 == True, 0 == False

`GOOGLE_REDIRECT_URL` = 'http://127.0.0.1:3000'

`ALLOWED_HOSTS` = '["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "192.168.1.7"]'


## Run Locally

Clone the project

```bash
  git clone git@github.com:vscubing/vscubing-backend.git -b dev
```

Go to the project directory

```bash
  cd vscubing-backend
```

Create venv (on linux)

```bash
  python3 -m venv venv
```


Activate venv (on linux)

```bash
  source venv/bing/activate
```

Install requirements

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```


## Contributing

Contributions are always welcome!

See [contributing.md](contributing.md) for ways to get started.



## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

