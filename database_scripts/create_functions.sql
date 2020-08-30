USE shopdb;
GO

-- This function calculates the total cost of the product in the purchase receipts,
-- it uses the discount of a discount card
CREATE OR ALTER FUNCTION compute_total_cost(@quantity INT, @price MONEY, @promotion NVARCHAR(30), @card_id INT)
RETURNS MONEY
    BEGIN
        DECLARE @index_of_discount INT = CHARINDEX('%', @promotion), @discount FLOAT,
            @total_cost MONEY = @price * @quantity, @quantity_discounted INT,
            @discount_card_discount FLOAT = 0
        IF @index_of_discount > 0
            BEGIN
                SET @discount = CAST(SUBSTRING(@promotion, 1, @index_of_discount - 1) AS FLOAT) / 100
                SET @total_cost = (@quantity * @price) * (1 - @discount)
            END
        IF @promotion = '1+1'
            BEGIN
                SET @quantity_discounted = @quantity / 2
                SET @total_cost = (@quantity - @quantity_discounted) * @price
            END
        IF @promotion = '2+1'
            BEGIN
                SET @quantity_discounted = @quantity / 3
                SET @total_cost = (@quantity - @quantity_discounted) * @price
            END

        SET @discount_card_discount = (
            SELECT discount
                FROM DiscountCards
                WHERE card_id = @card_id AND
                      is_blocked != 1)
        IF @discount_card_discount IS NULL
            SET @discount_card_discount = 0

        SET @total_cost = @total_cost * (1 - @discount_card_discount)
        RETURN @total_cost
    END