from celery import Celery

config = {
    "mongodb_scheduler_db": "kltn_db",
    "mongodb_scheduler_url": "mongodb://localhost:27017",
}

app = Celery('api', broker='amqp://guest:guest@localhost:5672/')
app.conf.update(**config)
app.autodiscover_tasks()

from celerybeatmongo.models import PeriodicTask

@app.task
def test_cel():
    print('test cel')

periodic = PeriodicTask(
    name='Importing contacts',
    task="api.celery.test_cel",
    interval=PeriodicTask.Interval(every=10, period="seconds") # executes every 10 seconds.
)
periodic.save()