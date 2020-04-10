-- CREATE DATABASE shop_db;

CREATE TABLE users -- пользователи системы
(
user_id      INT 
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
product_id   INT 
             PRIMARY KEY
             NOT NULL,
 
name         VARCHAR(64)
             UNIQUE
             NOT NULL
);

CREATE TABLE workers
(
worker_id    INT 
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
address_id   INT 
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
customer_id  INT 
             PRIMARY KEY
             NOT NULL,

user_id      INT
             REFERENCES users
             UNIQUE
             NOT NULL,

address_id   INT
             REFERENCES addresses,
		 
first_name   VARCHAR(16) 
             NOT NULL,
		 
second_name  VARCHAR(16) 
             NOT NULL
);

CREATE TABLE suppliers
(
supplier_id  INT 
             PRIMARY KEY
             NOT NULL,

user_id      INT
             REFERENCES users
             NOT NULL,
		 
product_id   INT
             REFERENCES products
             NOT NULL,

address_id   INT
             REFERENCES addresses,
		 
name         VARCHAR(128)
             NOT NULL
);

CREATE TABLE warehouses
(
warehouse_id INT
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
order_id     INT
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
delivery_id  INT
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

