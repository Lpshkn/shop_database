USE shopdb

CREATE TABLE DiscountCards
(
card_id      INT
             IDENTITY
             PRIMARY KEY,

discount     FLOAT
             NOT NULL
             DEFAULT 0,

start_date   DATE
             NOT NULL
             DEFAULT GETDATE(),

expiration   DATE
             NOT NULL
);

CREATE TABLE Customers
(
customer_id  INT
             IDENTITY
             PRIMARY KEY,

fullname     NVARCHAR(128)
             NOT NULL,

card_id      INT,

address      VARCHAR(128),
email        VARCHAR(128),

CONSTRAINT card_foreign FOREIGN KEY (card_id)
    REFERENCES DiscountCards(card_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Suppliers
(
supplier_id  INT
             IDENTITY
             PRIMARY KEY,

name         NVARCHAR(128)
             NOT NULL
             UNIQUE,

address      NVARCHAR(128)
             NOT NULL
);

CREATE TABLE Products
(
product_id   INT
             IDENTITY
             PRIMARY KEY,

name         NVARCHAR(128)
             NOT NULL
             UNIQUE,

company      NVARCHAR(128)
             NOT NULL,

quantity     SMALLINT
             NOT NULL,

supplier_name NVARCHAR(128)
             NOT NULL,

CONSTRAINT supplier_foreign FOREIGN KEY (supplier_name)
    REFERENCES Suppliers(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Purchases
(
purchase_id  INT
             NOT NULL
             UNIQUE,

product_id   INT
             NOT NULL,

quantity     SMALLINT
             NOT NULL,

cost         MONEY
             NOT NULL,

CONSTRAINT purchases_prim PRIMARY KEY (purchase_id, product_id),
CONSTRAINT product_foreign FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)

CREATE TABLE Workers
(
worker_id    INT
             IDENTITY
             PRIMARY KEY,

fullname     NVARCHAR(128)
             NOT NULL
             UNIQUE,

salary       MONEY,

job          NVARCHAR(32),

address      NVARCHAR(128)
             NOT NULL,

passport_number CHAR(10)
             NOT NULL
             UNIQUE
);

CREATE TABLE Receipts
(
receipt_id   INT
             IDENTITY
             PRIMARY KEY,

customer_id  INT
             NOT NULL,

purchase_id  INT
             NOT NULL,

worker_name  NVARCHAR(128),

date         DATETIME
             NOT NULL
             DEFAULT GETDATE(),

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
