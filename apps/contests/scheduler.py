import logging
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .general_services import generate_contest_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_contest():
    generate_contest_service(days_lasts=1)
    print('contest created')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        create_contest,
        trigger="cron",
        minute="*",
        id="create_contest",
        replace_existing=True,
        jobstore="default"
    )

    logger.info("Scheduler started and job added")
    scheduler.start()
