from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

from .scheduler_jobs import *

scheduler.add_job(FirstCronTest, 'interval', seconds=5)
scheduler.start()