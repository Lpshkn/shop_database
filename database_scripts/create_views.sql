USE shopdb;
GO

-- The view to show the purchases in the appropriate view for a user. Contains a list of products.
CREATE OR ALTER VIEW PurchaseView
    AS SELECT Customers.fullname customer_name, Workers.fullname worker_name, Products.name product_name,
              Purchases.quantity, Purchases.date, Purchases.total_cost
       FROM Customers, Purchases, Workers, Products
       WHERE Purchases.customer_id = Customers.customer_id AND
             Purchases.worker_id = Workers.worker_id AND
             Purchases.product_id = Products.product_id;
GO

-- The view to show the purchases receipts containing the total cost of the purchase
CREATE OR ALTER VIEW PurchaseReceipts
    AS SELECT customer_name, worker_name, date, SUM(total_cost) total_cost
       FROM PurchaseView
       GROUP BY customer_name, worker_name, date;
GO

-- The view to show a list of workers, their job and email. This information will be available for administrator
CREATE OR ALTER VIEW WorkersView
    AS SELECT fullname, job, email
       FROM Workers
GO

