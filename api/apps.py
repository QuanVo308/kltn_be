from django.apps import AppConfig
import os
import sys

def startup():
    print('startup')
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    # startup()
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        startup()
