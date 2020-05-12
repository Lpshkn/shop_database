import pymssql

_conn: pymssql.Connection = None


def set_conn(**kwargs):
    global _conn
    _conn = MssqlStorage.connect_to_db(**kwargs)


def get_conn():
    global _conn
    return _conn


def close_conn():
    global _conn
    if _conn:
        _conn.close()


class MssqlStorage:

    _conn = pymssql.Connection
    _cur = pymssql.Cursor

    @staticmethod
    def connect_to_db(server: str, user: str, password: str, dbname: str):
        return pymssql.connect(server, user, password, dbname)


class WorkersStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = WorkersStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_workers(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Workers')
        workers = []
        row = self._cur.fetchone()
        while row:
            workers.append(row)
            row = self._cur.fetchone()
        return workers
