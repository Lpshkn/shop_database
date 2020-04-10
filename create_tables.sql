-- CREATE DATABASE shop_db;

CREATE TABLE users -- пользователи системы
(
id           INT 
             PRIMARY KEY
             NOT NULL,
 
username     VARCHAR(64)
             UNIQUE
             NOT NULL,

pass_hash    VARCHAR(128)
             NOT NULL
);

CREATE TABLE products  
(
id           INT 
             PRIMARY KEY
             NOT NULL,
 
name         VARCHAR(64)
             UNIQUE
             NOT NULL
);

CREATE TABLE workers
(
id           INT 
             PRIMARY KEY
             NOT NULL,

user_id      INT
             REFERENCES users
             UNIQUE
             NOT NULL,
		
first_name   VARCHAR(16)
             NOT NULL,

second_name  VARCHAR(16)
             NOT NULL,
		
salary       INT,
		
position     VARCHAR(32)
);

CREATE TABLE addresses
(
id           INT 
             PRIMARY KEY
             NOT NULL,

city         VARCHAR(32)
             NOT NULL,

country      VARCHAR(32)
             NOT NULL,
		 
postal_code  VARCHAR(16)
             UNIQUE
             NOT NULL
);

CREATE TABLE customers
(
id           INT 
             PRIMARY KEY
             NOT NULL,

user_id      INT
             REFERENCES users
             UNIQUE
             NOT NULL,

address_id   INT
             REFERENCES addresses
             NOT NULL,
		 
first_name   VARCHAR(16) 
             NOT NULL,
		 
second_name  VARCHAR(16) 
             NOT NULL
);

CREATE TABLE suppliers
(
id           INT 
             PRIMARY KEY
             NOT NULL,

user_id      INT
             REFERENCES users
             NOT NULL,
		 
product_id   INT
             REFERENCES products
             NOT NULL,

address_id   INT
             REFERENCES addresses
             NOT NULL,
		 
name         VARCHAR(128)
             NOT NULL
);

CREATE TABLE warehouse
(
id           INT
             PRIMARY KEY
             NOT NULL,
   
product_id   INT
             REFERENCES products
             UNIQUE
             NOT NULL,
		 
quantity     INT
             NOT NULL
);

CREATE TABLE orders -- покупка товара клиентом
(
id           INT
             PRIMARY KEY
             NOT NULL,

product_id   INT
             REFERENCES products
             NOT NULL,
			
customer_id  INT
             REFERENCES customers
             NOT NULL,
			
quantity     INT
             NOT NULL,
		   
cost         INT
             NOT NULL,

date         TIMESTAMP
);

CREATE TABLE deliveries -- заказ товара у поставщика
(
id           INT
             PRIMARY KEY
             NOT NULL,

product_id   INT
             REFERENCES products
             NOT NULL,
			
supplier_id  INT
             REFERENCES suppliers
             NOT NULL,
			
quantity     INT
             NOT NULL,
		   
cost         INT
             NOT NULL,

date         TIMESTAMP
);

