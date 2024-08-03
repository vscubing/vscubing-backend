from vscubing.celery import app
from .general_services import generate_contest_service

@app.task
def create_contest():
    generate_contest_service(days_lasts=1)
