USE shopdb;
GO

-- This procedure clears all the promotions of an each product
CREATE OR ALTER PROCEDURE clear_promotions
    AS UPDATE Products
        SET promotion = NULL;
GO

-- This procedure sets all the promotions to the @promotion value
CREATE OR ALTER PROCEDURE setup_all_promotions (@promotion NVARCHAR(30))
    AS UPDATE Products
        SET promotion = @promotion;
GO

-- This procedure make the special discount card blocked or not
CREATE OR ALTER PROCEDURE block_discount_car (@card_id INT, @block BIT)
    AS UPDATE DiscountCards
        SET is_blocked = @block
        WHERE card_id = @card_id;
GO