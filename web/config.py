import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MSSQL_USER = os.environ.get('MSSQL_USER') or 'SA'
    MSSQL_PW = os.environ.get('MSSQL_PW')
    MSSQL_HOST = os.environ.get('MSSQL_HOST') or 'leadness.keenetic.name'
    MSSQL_PORT = os.environ.get('MSSQL_PORT')
    MSSQL_DB = os.environ.get('MSSQL_DB') or 'shopdb'
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://{user}:{pw}@{host}:{port}/{db}'.format(
        user=MSSQL_USER, pw=MSSQL_PW, host=MSSQL_HOST, port=MSSQL_PORT, db=MSSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
