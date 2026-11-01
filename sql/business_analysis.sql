-- Business analysis queries for the cleaned used-car dataset.
-- Assumes a table named used_cars (load data/processed/used_cars_cleaned.csv).

-- 1. Market overview: inventory, price, and mileage distribution
SELECT
    COUNT(*)                       AS total_listings,
    COUNT(DISTINCT make)           AS brands,
    COUNT(DISTINCT model)          AS models,
    ROUND(AVG(price), 2)           AS avg_price,
    ROUND(MIN(price), 2)           AS min_price,
    ROUND(MAX(price), 2)           AS max_price,
    ROUND(AVG(mileage), 0)         AS avg_mileage
FROM used_cars;

-- 2. Average price by brand, ranked
SELECT
    make,
    COUNT(*)                 AS listings,
    ROUND(AVG(price), 2)     AS avg_price,
    ROUND(AVG(mileage), 0)   AS avg_mileage
FROM used_cars
GROUP BY make
HAVING COUNT(*) >= 10
ORDER BY avg_price DESC;

-- 3. Price and mileage by model year
SELECT
    year,
    COUNT(*)                 AS listings,
    ROUND(AVG(price), 2)     AS avg_price,
    ROUND(AVG(mileage), 0)   AS avg_mileage
FROM used_cars
GROUP BY year
ORDER BY year;

-- 4. Depreciation: average price by vehicle age
SELECT
    EXTRACT(YEAR FROM CURRENT_DATE) - year AS vehicle_age,
    COUNT(*)                              AS listings,
    ROUND(AVG(price), 2)                  AS avg_price
FROM used_cars
GROUP BY EXTRACT(YEAR FROM CURRENT_DATE) - year
ORDER BY vehicle_age;

-- 5. Fuel type and transmission mix
SELECT
    fuel_type,
    transmission,
    COUNT(*)              AS listings,
    ROUND(AVG(price), 2)  AS avg_price
FROM used_cars
GROUP BY fuel_type, transmission
ORDER BY listings DESC;

-- 6. Seller analysis: volume and average price by seller type
SELECT
    seller_type,
    COUNT(*)                          AS listings,
    ROUND(AVG(price), 2)              AS avg_price,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_listings
FROM used_cars
GROUP BY seller_type
ORDER BY listings DESC;

-- 7. Geographic analysis: top locations by listing volume
SELECT
    location,
    COUNT(*)              AS listings,
    ROUND(AVG(price), 2)  AS avg_price
FROM used_cars
GROUP BY location
ORDER BY listings DESC
LIMIT 20;

-- 8. Best-value listings: newest and lowest mileage per brand
SELECT make, model, year, mileage, price
FROM (
    SELECT
        make,
        model,
        year,
        mileage,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY make
            ORDER BY year DESC, mileage ASC
        ) AS rn
    FROM used_cars
) ranked
WHERE rn = 1
ORDER BY make;

-- 9. Quartile-based price segmentation
SELECT
    NTILE(4) OVER (ORDER BY price) AS price_quartile,
    COUNT(*)                       AS listings,
    ROUND(MIN(price), 2)           AS min_price,
    ROUND(MAX(price), 2)           AS max_price
FROM used_cars
GROUP BY NTILE(4) OVER (ORDER BY price)
ORDER BY price_quartile;
