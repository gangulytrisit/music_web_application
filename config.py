import os
from dotenv import load_dotenv
load_dotenv()
from pytz import timezone

class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///trisit.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'trisit')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'thisissaltt_trisit')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CELERY_TIMEZONE = timezone("Asia/Kolkata")
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_TYPE= 'RedisCache'
    CACHE_DEFAULT_TIMEOUT= 200
    
    