from celery import Celery
from flask import current_app as app


#celery setup

celery = Celery("Application Jobs")
    
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)
