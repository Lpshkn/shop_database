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
            row = [item or '-' for item in row]
            workers.append(row)
            row = self._cur.fetchone()
        return workers


class SuppliersStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = SuppliersStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_suppliers(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Suppliers')
        suppliers = []
        row = self._cur.fetchone()
        while row:
            row = [item or '-' for item in row]
            suppliers.append(row)
            row = self._cur.fetchone()
        return suppliers


class ProductsStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = ProductsStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_products(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Products')
        products = []
        row = self._cur.fetchone()
        while row:
            row = [item or '-' for item in row]
            products.append(row)
            row = self._cur.fetchone()
        return products


class CustomersStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = CustomersStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_customers(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Customers')
        customers = []
        row = self._cur.fetchone()
        while row:
            row = [item or '-' for item in row]
            customers.append(row)
            row = self._cur.fetchone()
        return customers


class DiscountCardsStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = DiscountCardsStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_cards(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.DiscountCards')
        cards = []
        row = self._cur.fetchone()
        while row:
            cards.append(row)
            row = self._cur.fetchone()
        return cards


class ProducersStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = ProducersStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_producers(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Producers')
        producers = []
        row = self._cur.fetchone()
        while row:
            row = [item or '-' for item in row]
            producers.append(row)
            row = self._cur.fetchone()
        return producers


class PurchasesStorage(MssqlStorage):

    @staticmethod
    def get_connection(conn: pymssql.Connection):
        obj = PurchasesStorage()
        obj._conn = conn
        obj._cur = conn.cursor()
        return obj

    def get_purchases(self) -> list:
        self._cur.execute('SELECT * FROM shopdb.dbo.Purchases')
        purchases = []
        row = self._cur.fetchone()
        while row:
            row = [item or '-' for item in row]
            purchases.append(row)
            row = self._cur.fetchone()
        return purchases
