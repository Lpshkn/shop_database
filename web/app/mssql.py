import pymssql
from flask import flash, redirect, url_for
from functools import wraps
from datetime import datetime

_conn: pymssql.Connection = None


def check_conn(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except AttributeError:
            flash('Connection to database lost')
            return redirect(url_for('login'))
    return wrapper_func


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

    _conn: pymssql.Connection
    _cur:  pymssql.Cursor

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

    def get_workers_ids(self) -> list:
        return [row[0] for row in self.get_workers()]

    def delete_worker(self, worker_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Workers 
                  WHERE
                    worker_id = {worker_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_worker(self, fullname: str, salary: float, job: str, address: str,
                   passport_number: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO 
                    shopdb.dbo.Workers(fullname, salary, job, address, passport_number, telephone, email)
                  VALUES
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

    def get_suppliers_names(self) -> list:
        return [row[1] for row in self.get_suppliers()]

    def delete_supplier(self, supplier_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Workers 
                  WHERE
                    supplier_id = {supplier_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_supplier(self, name: str, address: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO
                    shopdb.dbo.Suppliers(name, address, email, telephone)
                  VALUES
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

    def get_products_ids(self) -> list:
        return [row[0] for row in self.get_products()]

    def delete_product(self, product_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Products 
                  WHERE
                    product_id = {product_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_product(self, name: str, producer: str, quantity: int, supplier: str, price: float, promotion: str) -> None:
        sql = f"""INSERT INTO 
                    shopdb.dbo.Products(name, producer, quantity, supplier, price)
                  VALUES
                    (N'{name}', N'{producer}', {quantity}, N'{supplier}', {price}, '{promotion}')"""
        self._cur.execute(sql)
        self._conn.commit()


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

    def get_customers_ids(self) -> list:
        return [row[0] for row in self.get_customers()]

    def delete_customer(self, customer_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Customers 
                  WHERE
                    customer_id = {customer_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_customer(self, fullname: str, card_id: int, address: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO
                    shopdb.dbo.Customers(fullname, address, card_id, email, telephone)
                  VALUES
                    (N'{fullname}', N'{address}', {card_id}, '{email}', '{telephone}')"""
        self._cur.execute(sql)
        self._conn.commit()


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

    def get_cards_ids(self) -> list:
        return [row[0] for row in self.get_cards()]

    def delete_card(self, card_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.DiscountCards 
                  WHERE
                    card_id = {card_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_card(self, discount: float, start_date: datetime, expiration: datetime) -> None:
        sql = f"""INSERT INTO
                    shopdb.dbo.DiscountCards(discount, start_date, expiration)
                  VALUES
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

    def get_producers_names(self) -> list:
        return [row[1] for row in self.get_producers()]

    def delete_producer(self, producer_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Producers 
                  WHERE
                    producer_id = {producer_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_producer(self, name: str, address: str, telephone: str, email: str) -> None:
        sql = f"""INSERT INTO 
                    shopdb.dbo.Producers(name, address, email, telephone)
                  VALUES
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

    def delete_purchase(self, purchase_id: int) -> None:
        sql = f"""DELETE 
                  FROM
                    shopdb.dbo.Purchases 
                  WHERE
                    purchase_id = {purchase_id}"""
        self._cur.execute(sql)
        self._conn.commit()

    def add_purchase(self, product_id: int, worker_id: int, customer_id: int,
                     quantity: int, total_cost: float, date: datetime) -> None:
        sql = f"""INSERT INTO 
                    shopdb.dbo.Purchases(product_id, worker_id, customer_id, quantity, total_cost, date)
                  VALUES
                    ({product_id}, {worker_id}, {customer_id}, {quantity}, {total_cost}, '{date}')"""
        self._cur.execute(sql)
        self._conn.commit()
