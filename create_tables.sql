USE shop_db

CREATE TABLE discount_cards
(
card_id INT IDENTITY PRIMARY KEY,
discount TINYINT NOT NULL DEFAULT 0,
start_date DATE NOT NULL DEFAULT GETDATE(),
expiration DATE NOT NULL
);

CREATE TABLE customers
(
customer_id INT IDENTITY PRIMARY KEY,
fullname VARCHAR(128) NOT NULL,
card_id INT,

CONSTRAINT card_foreign FOREIGN KEY (card_id)
    REFERENCES discount_cards(card_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE suppliers
(
supplier_id INT IDENTITY PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE,
address VARCHAR(255) NOT NULL
);

CREATE TABLE products
(
product_id INT IDENTITY PRIMARY KEY,
name VARCHAR(255) NOT NULL UNIQUE,
quantity_stock SMALLINT NOT NULL,
supplier_name VARCHAR(255) NOT NULL,

CONSTRAINT supplier_foreign FOREIGN KEY (supplier_name)
    REFERENCES suppliers(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE purchases
(
purchase_id INT NOT NULL UNIQUE,
product_id INT NOT NULL,
quantity SMALLINT NOT NULL,
default_cost MONEY NOT NULL,

CONSTRAINT purchases_prim PRIMARY KEY (purchase_id, product_id),
CONSTRAINT product_foreign FOREIGN KEY (product_id)
    REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)

CREATE TABLE workers
(
worker_id INT IDENTITY PRIMARY KEY,
fullname VARCHAR(128) NOT NULL UNIQUE,
salary MONEY,
job VARCHAR(32)
);

CREATE TABLE receipts
(
receipt_id INT IDENTITY PRIMARY KEY,
customer_id INT NOT NULL,
purchase_id INT NOT NULL,
worker_name VARCHAR(128),
date DATETIME,

CONSTRAINT fullname_foreign FOREIGN KEY (worker_name)
    REFERENCES workers(fullname)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

CONSTRAINT customer_foreign FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

CONSTRAINT purchase_foreign FOREIGN KEY (purchase_id)
    REFERENCES purchases(purchase_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
