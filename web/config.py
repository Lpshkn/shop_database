import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
    POSTGRES_PW = os.environ.get('POSTGRES_PW') or 'password'
    POSTGRES_URL = os.environ.get('POSTGRES_URL') or '172.17.0.2:5432'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'postgres'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
