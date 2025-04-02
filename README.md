
# vscubing api

RESTful api for vscubing.com powered with Django Rest Framework


## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Tech Stack

Django, Django Rest Framework


## Authors

- [@HomaDev](https://github.com/HomaDev)

## Run Locally

- Clone the project **!!!WITH SUBMODULES!!!**

```bash
  git clone --recurse-submodules git@github.com:vscubing/vscubing-backend.git -b dev
```

If you have already cloned the project without `--recurse-submodules`, run `git submodule update --init --recursive` to clone the submodules.

- Build twsearch
```bash
  cd vendor/twsearch && make build && cd ../../
```

- Create venv (on linux)

```bash
  python3 -m venv venv
```

- Activate venv (on linux)

```bash
  source venv/bin/activate
  # using fish shell: `source venv/bin/activate.fish`
```

- Install requirements

```bash
  pip install -r requirements.txt
```

- Add and populate `.env` (refer to `.example-env`)

- Run migrations
```bash
  python3 manage.py migrate
```

- To create fake data for test use, utilize this command
```bash
  python3 manage.py generate_full_data
```
**There are some parms that can be used**

how many users to generate
`--users_qty int`

disciplines names to generate 
`--discipline_names str str str`

amount of scrumbles to create new contests (after initial generation)
`--tnoodle_scrambles_qty int`

how many moves each new contest scramble with have 
`--tnoodle_scrambles_moves_qty int`

how many moves past contests' scrambles and current contest's scramble have 
`--scrambles_moves_qty int`

how many past contests to generate 
`--contest_qty int`


Example
```bash
python3 manage.py generate_full_data --users_qty 15 --discipline_names 3by3 2by2 --tnoodle_scrambles_qty 20 --contest_qty 5 --tnoodle_scrambles_moves_qty 8 --scrambles_moves_qty 10 ```



- Start the server

```bash
  python3 manage.py runserver
```

- (Optional) Start celery worker and beat
```bash
celery -A vscubing.celery worker --loglevel=info
celery -A vscubing.celery beat --loglevel=info
```

## Contributing

Contributions are always welcome!


## Support

For support, email savytskyi.work@gmail.com
