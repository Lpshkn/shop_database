import pymssql
from datetime import datetime

_conn: pymssql.Connection = None


def set_conn(**kwargs) -> None:
    global _conn
    _conn = MssqlStorage.connect_to_db(**kwargs)


def get_conn() -> pymssql.Connection:
    global _conn
    return _conn


def close_conn() -> None:
    global _conn
    if _conn:
        _conn.close()


class MssqlStorage:

    _conn = pymssql.Connection
    _cur = pymssql.Cursor

    @staticmethod
    def connect_to_db(server: str, user: str, password: str, dbname: str) -> pymssql.Connection:
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

    def add_worker(self, fullname: str, salary: float, job: str, address: str,
                   passport_number: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO shopdb.dbo.Workers 
                  (fullname, salary, job, address, passport_number, telephone, email) VALUES
                  (N'{fullname}', {salary}, N'{job}', N'{address}', '{passport_number}', '{telephone}', '{email}')"""
        self._cur.execute(sql)
        self._conn.commit()


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

    def add_supplier(self, name: str, address: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO shopdb.dbo.Suppliers 
                  (name, address, email, telephone) VALUES
                  (N'{name}', N'{address}', '{email}', '{telephone}')"""
        self._cur.execute(sql)
        self._conn.commit()


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

    def add_card(self, discount: float, start_date: datetime, expiration: datetime) -> None:
        sql = f"""INSERT INTO shopdb.dbo.DiscountCards 
                  (discount, start_date, expiration) VALUES
                  ('{discount}', '{start_date}', '{expiration}')"""
        self._cur.execute(sql)
        self._conn.commit()


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

    def add_producer(self, name: str, address: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO shopdb.dbo.Producers 
                  (name, address, email, telephone) VALUES
                  (N'{name}', N'{address}', '{email}', '{telephone}')"""
        self._cur.execute(sql)
        self._conn.commit()


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
