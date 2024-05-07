from flask import Flask
from flask_security import Security, hash_password
from flask_cors import CORS
from api import api
from model import db, User, Role
from flask_security.datastore import SQLAlchemyUserDatastore
from celery import Celery
from celery.schedules import crontab
from cache import cache
import workers
from config import DevelopmentConfig
from task import daily_rem, month_rep



import datetime
import pytz 



datastore=SQLAlchemyUserDatastore(db,User,Role)


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    api.init_app(app)
    #cache initiation
    cache.init_app(app)
    #Create celery
    celery=workers.celery
    app.app_context().push()
    #update with configuration
    celery.conf.update(
     broker_url= app.config["CELERY_BROKER_URL"],
     result_backend = app.config["CELERY_RESULT_BACKEND"],
    #  timezone='Asia/Kolkata',
    #  CELERY_ENABLE_UTC=False
    )
    celery.Task=workers.ContextTask
    app.app_context().push()
    CORS(app)



    app.security = Security(app, datastore)
    return app, celery

app, celery = create_app()

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin', description="admin is an admin")
    datastore.find_or_create_role(name='creator', description="creator is a creator")
    datastore.find_or_create_role(name='user', description="User is a user")
    db.session.commit()
    for email, username, password, roles, active, flag in [
        ("admin@admin.com", "admin", "admin123", ["admin"], True, True),
        ("creator@creator.com", "Creator", "creator123", ["creator"], True, True),
        ("user@user.com", "User", "user123", ["user"], True, True)
    ]:
        if not datastore.find_user(email=email):
            datastore.create_user(
                username=username,
                email=email,
                password=hash_password(password),
                roles=roles,
                active=active,
                flag=flag
            )
    db.session.commit()



# scheudled time for daily reminder 
daily_reminder_schedule = crontab(hour=14, minute=30)

#  scheduled time  for the monthly 
monthly_report_schedule = crontab(hour=15, minute=00, day_of_month=1)

celery.conf.beat_schedule = {
    'automate_daily_email_user': {
        'task': 'task.daily_rem',
        'schedule': daily_reminder_schedule
    },
    'automate_monthly_email_creator': {
        'task': 'task.month_rep',
        'schedule': monthly_report_schedule
    },
}



    


if __name__ == '__main__':
    app.run(debug=True)