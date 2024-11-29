import os
from django.apps import AppConfig
from utils.db_utils import setup_database


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Check for the main process
        if os.environ.get('RUN_MAIN') == 'true':
            setup_database()
