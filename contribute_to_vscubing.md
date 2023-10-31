### Contribute to Vscode



### starting
Start with cloning repo

```commandline
git clone git@github.com:vscubing/vscubing-backend.git -b dev
```

Access repo

```commandline
cd vscubing-backend
```

Create python venv and activate it (if you are using linux, else find another way)

```commandline
python -m venv venv
source venv/bing/activate
```

Install all dependencies 

```commandline
pip install -r requirements.txt
```

Next you need to setup .env like .example-env

And run server

```commandline
python manage.py runserver
```