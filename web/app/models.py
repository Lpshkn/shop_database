from datetime import datetime
from app import db


class DiscountCard(db.Model):
    __tablename__ = 'DiscountCards'
    card_id = db.Column(db.INT, primary_key=True)
    discount = db.Column(db.FLOAT, nullable=False, default=0.0)
    start_date = db.Column(db.DATE, nullable=False, default=datetime.utcnow)
    expiration = db.Column(db.DATE, nullable=False)
    customer = db.relationship('Customer',
                               backref='card_foreign',
                               uselist=False)

    def __repr__(self):
        return f'<DiscountCard: {self.card_id}>'


class Customer(db.Model):
    __tablename__ = 'Customers'
    customer_id = db.Column(db.INT, primary_key=True)
    address = db.Column(db.NVARCHAR(128), nullable=False)
    fullname = db.Column(db.NVARCHAR(128), nullable=False)
    email = db.Column(db.VARCHAR(128), unique=True)
    telephone = db.Column(db.VARCHAR(16), unique=True)
    card_id = db.Column(db.INT,
                        db.ForeignKey('DiscountCards.card_id', ondelete='CASCADE', onupdate='CASCADE'),
                        name='card_foreign',
                        nullable=False)
    purchases = db.relationship('Purchase',
                                backref='customer_foreign')

    def __repr__(self):
        return f'<Customer: {self.fullname}>'


class Supplier(db.Model):
    __tablename__ = 'Suppliers'
    supplier_id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(128), unique=True, nullable=False)
    address = db.Column(db.NVARCHAR(128), nullable=False)
    email = db.Column(db.VARCHAR(128), unique=True)
    telephone = db.Column(db.VARCHAR(16), unique=True)
    products = db.relationship('Product',
                               backref='supplier_foreign')

    def __repr__(self):
        return f'<Supplier: {self.name}>'


class Producer(db.Model):
    __tablename__ = 'Producers'
    producer_id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(128), unique=True, nullable=False)
    address = db.Column(db.NVARCHAR(128), nullable=False)
    email = db.Column(db.VARCHAR(128), unique=True)
    telephone = db.Column(db.VARCHAR(16), unique=True)
    products = db.relationship('Product',
                               backref='producer_foreign')

    def __repr__(self):
        return f'<Producer: {self.name}>'


class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(128), index=True, unique=True, nullable=False)
    cost = db.Column(db.FLOAT, nullable=False)
    quantity = db.Column(db.SMALLINT, nullable=False)
    supplier = db.Column(db.NVARCHAR(128),
                         db.ForeignKey('Suppliers.name', ondelete='CASCADE', onupdate='CASCADE'),
                         name='supplier_foreign',
                         nullable=False)
    producer = db.Column(db.NVARCHAR(128),
                         db.ForeignKey('Producers.name', ondelete='CASCADE', onupdate='CASCADE'),
                         name='producer_foreign',
                         nullable=False)
    purchases = db.relationship('Purchase',
                                backref='product_foreign')

    def __repr__(self):
        return '<Product: {}>'.format(self.name)


class Worker(db.Model):
    __tablename__ = 'Workers'
    worker_id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.VARCHAR(10), unique=True, nullable=False)
    fullname = db.Column(db.NVARCHAR(128), unique=True, nullable=False)
    salary = db.Column(db.FLOAT)
    job = db.Column(db.NVARCHAR(32))
    address = db.Column(db.NVARCHAR(128), nullable=False)
    email = db.Column(db.VARCHAR(128), unique=True, nullable=False)
    telephone = db.Column(db.VARCHAR(16), unique=True)
    purchases = db.relationship('Purchase',
                                backref='worker_foreign')

    def __repr__(self):
        return f'<Worker: {self.fullname}>'


class Purchase(db.Model):
    __tablename__ = 'Purchases'
    purchase_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.SMALLINT, nullable=False)
    date = db.Column(db.DATE, nullable=False, default=datetime.utcnow)
    total_cost = db.Column(db.FLOAT, nullable=False)
    product_id = db.Column(db.INT,
                           db.ForeignKey('Products.product_id', ondelete='CASCADE', onupdate='CASCADE'),
                           name='product_foreign',
                           nullable=False)
    worker_id = db.Column(db.INT,
                          db.ForeignKey('Workers.worker_id', ondelete='SET NULL', onupdate='CASCADE'),
                          name='worker_foreign')
    customer_id = db.Column(db.INT,
                            db.ForeignKey('Customers.customer_id', ondelete='CASCADE', onupdate='CASCADE'),
                            name='customer_foreign')

    def __repr__(self):
        return f'<Purchase: {self.purchase_id}>'
