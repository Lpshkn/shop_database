import pymssql

db = None


def set_db(**kwargs):
    global db
    db = MssqlStorage.get_connection(**kwargs)


def get_db():
    global db
    return db


def close_db():
    global db
    if db:
        db.close()


class MssqlStorage:

    _server = ''
    _user = ''
    _password = ''
    _dbname = ''
    _conn = pymssql.Connection

    @staticmethod
    def get_connection(server: str, user: str, password: str, dbname: str):
        return pymssql.connect(server, user, password, dbname)

    def __del__(self):
        self._conn.close()

    def __repr__(self):
        return 'MssqlStorage: {}:{}@{}/{}'.format(
            self._user, self._password, self._server, self._dbname)
