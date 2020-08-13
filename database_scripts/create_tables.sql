IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'shopdb')
    BEGIN
        CREATE DATABASE shopdb
    END

USE shopdb
EXECUTE sys.sp_cdc_enable_db;

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DiscountCards')
    BEGIN
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
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Customers')
    BEGIN
        CREATE TABLE Customers
        (
        customer_id  INT
                     IDENTITY
                     PRIMARY KEY,

        fullname     NVARCHAR(128)
                     NOT NULL,

        card_id      INT,

        address      VARCHAR(128)
                     NOT NULL,

        email        VARCHAR(128)
                     UNIQUE,

        telephone    VARCHAR(16)
                     UNIQUE,

        CONSTRAINT card_foreign FOREIGN KEY (card_id)
            REFERENCES DiscountCards(card_id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
        );
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Suppliers')
    BEGIN
        CREATE TABLE Suppliers
        (
        supplier_id  INT
                     IDENTITY
                     PRIMARY KEY,

        name         NVARCHAR(128)
                     NOT NULL
                     UNIQUE,

        address      NVARCHAR(128)
                     NOT NULL,

        email        VARCHAR(128)
                     UNIQUE,

        telephone    VARCHAR(16)
                     UNIQUE
        );
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Producers')
    BEGIN
        CREATE TABLE Producers
        (
        producer_id  INT
                     IDENTITY
                     PRIMARY KEY,

        name         NVARCHAR(128)
                     NOT NULL
                     UNIQUE,

        address      NVARCHAR(128)
                     NOT NULL,

        email        VARCHAR(128)
                     UNIQUE,

        telephone    VARCHAR(16)
                     UNIQUE
        )
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Products')
    BEGIN
        CREATE TABLE Products
        (
        product_id   INT
                     IDENTITY
                     PRIMARY KEY,

        name         NVARCHAR(128)
                     NOT NULL
                     UNIQUE,

        producer     NVARCHAR(128)
                     NOT NULL,

        quantity     SMALLINT
                     NOT NULL,

        supplier     NVARCHAR(128)
                     NOT NULL,

        price        MONEY
                     NOT NULL,

        promotion    NVARCHAR(30),

        CONSTRAINT supplier_foreign FOREIGN KEY (supplier)
            REFERENCES Suppliers(name)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

        CONSTRAINT producer_foreign FOREIGN KEY (producer)
            REFERENCES Producers(name)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Workers')
    BEGIN
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
                     UNIQUE,

        telephone    VARCHAR(16)
                     UNIQUE,

        email        VARCHAR(128)
                     NOT NULL
                     UNIQUE
        );
    END

IF NOT EXISTS(SELECT * FROM shopdb.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Purchases')
    BEGIN
        CREATE TABLE Purchases
        (
        purchase_id  INT
                     IDENTITY
                     PRIMARY KEY,

        product_id   INT
                     NOT NULL,

        worker_id    INT,

        customer_id  INT
                     NOT NULL,

        quantity     SMALLINT
                     NOT NULL,

        date         DATETIME
                     NOT NULL
                     DEFAULT GETDATE(),

        total_cost   MONEY
                     NOT NULL,

        CONSTRAINT product_foreign FOREIGN KEY (product_id)
            REFERENCES Products(product_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

        CONSTRAINT worker_foreign FOREIGN KEY (worker_id)
            REFERENCES Workers(worker_id)
                ON DELETE SET NULL
                ON UPDATE CASCADE,

        CONSTRAINT customer_foreign FOREIGN KEY (customer_id)
            REFERENCES Customers(customer_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    END
