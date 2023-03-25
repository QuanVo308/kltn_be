from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

from .scheduler_jobs import *

# scheduler.add_job(FirstCronTest, 'interval', seconds=1)
scheduler.add_job(FirstCronTest, 'interval', seconds=10, jitter=2)
scheduler.add_job(FirstCronTest2, 'interval', seconds=10)
scheduler.start()