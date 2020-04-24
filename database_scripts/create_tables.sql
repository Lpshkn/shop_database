USE shop_db

CREATE TABLE Discount_cards
(
card_id INT IDENTITY PRIMARY KEY,
discount TINYINT NOT NULL DEFAULT 0,
start_date DATE NOT NULL DEFAULT GETDATE(),
expiration DATE NOT NULL
);

CREATE TABLE Customers
(
customer_id INT IDENTITY PRIMARY KEY,
fullname VARCHAR(128) NOT NULL,
card_id INT,

CONSTRAINT card_foreign FOREIGN KEY (card_id)
    REFERENCES discount_cards(card_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Suppliers
(
supplier_id INT IDENTITY PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE,
address VARCHAR(255) NOT NULL
);

CREATE TABLE Products
(
product_id INT IDENTITY PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE,
quantity_stock SMALLINT NOT NULL,
supplier_name VARCHAR(255) NOT NULL,

CONSTRAINT supplier_foreign FOREIGN KEY (supplier_name)
    REFERENCES Suppliers(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Purchases
(
purchase_id INT NOT NULL UNIQUE,
product_id INT NOT NULL,
quantity SMALLINT NOT NULL,
default_cost MONEY NOT NULL,

CONSTRAINT purchases_prim PRIMARY KEY (purchase_id, product_id),
CONSTRAINT product_foreign FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)

CREATE TABLE Workers
(
worker_id INT IDENTITY PRIMARY KEY,
fullname VARCHAR(128) NOT NULL UNIQUE,
salary MONEY,
job VARCHAR(32)
);

CREATE TABLE Receipts
(
receipt_id INT IDENTITY PRIMARY KEY,
customer_id INT NOT NULL,
purchase_id INT NOT NULL,
worker_name VARCHAR(128),
date DATETIME,

CONSTRAINT fullname_foreign FOREIGN KEY (worker_name)
    REFERENCES Workers(fullname)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

CONSTRAINT customer_foreign FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

CONSTRAINT purchase_foreign FOREIGN KEY (purchase_id)
    REFERENCES Purchases(purchase_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
