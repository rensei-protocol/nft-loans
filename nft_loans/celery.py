import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nft_loans.settings")

app = Celery("nft_loans")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# Scheduler
FETCHER_PERIOD_SEC = int(os.getenv("FETCHER_PERIOD_SEC", 30))  # default is 30
app.conf.beat_schedule = {
    "x2y2_fetch": {
        "task": "x2y2_fetch_task",
        "schedule": FETCHER_PERIOD_SEC,
    },
    "nftfi_fetch": {
        "task": "nftfi_fetch_task",
        "schedule": FETCHER_PERIOD_SEC,
    },
    "arcade_fetch": {
        "task": "arcade_fetch_task",
        "schedule": FETCHER_PERIOD_SEC,
    },
    "benddao_fetch": {
        "task": "benddao_fetch_task",
        "schedule": FETCHER_PERIOD_SEC,
    },
}
