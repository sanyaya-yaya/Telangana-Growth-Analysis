CREATE DATABASE Telengana_growth;
Use Telengana_growth;

-- Total documents revenue

SELECT
    d.district,
    SUM(fs.documents_registered_rev) AS total_revenue
FROM
    fact_stamps fs
JOIN
    district_names d
ON
    fs.dist_code = d.dist_code
GROUP BY
    d.district
ORDER BY
    total_revenue DESC;



  -- PERCENTAGE OF TOTAL and top 5 district with highest revenue for the year 2019-2022

SELECT
    d.district,
    SUM(fs.documents_registered_rev) AS total_revenue,
    (SUM(fs.documents_registered_rev) / (SELECT SUM(documents_registered_rev) FROM fact_stamps)) * 100 AS percentage_of_total
FROM
    fact_stamps fs
JOIN
    district_names d
ON
    fs.dist_code = d.dist_code
GROUP BY
    d.district
ORDER BY
    total_revenue DESC
LIMIT 
     5;

-- the top 5 districts where e-stamps revenue contributes significantly more to the revenue than the documents in FY 2022 --

SELECT
    ds.district,
    SUM(s.documents_registered_rev) AS document_registration_revenue,
    SUM(s.estamps_challans_rev) AS estamps_revenue
FROM
    fact_stamps s
JOIN
    district_names ds ON s.dist_code = ds.dist_code
JOIN
    Date d ON s.month = d.month
WHERE
    d.fiscal_year = 2022
GROUP BY
    ds.district
HAVING
    SUM(s.estamps_challans_rev) > 1 * SUM(s.documents_registered_rev) -- Adjust the threshold as needed
ORDER BY
    SUM(s.estamps_challans_rev) DESC
LIMIT
    5;

-- Is there any alteration of e-Stamp challan count and document registration count pattern since the implementation of e-Stamp challan? 
SELECT
    DATE_FORMAT(month, '%Y-%m') AS period,
    'Before Implementation' AS implementation_phase,
    SUM(estamps_challans_cnt) AS estamps_challans_count,
    SUM(documents_registered_cnt) AS documents_registered_count
FROM
    fact_stamps
WHERE
    month < '2020-01-01'
GROUP BY
    DATE_FORMAT(month, '%Y-%m')

UNION ALL

-- Calculate counts after e-Stamp challan implementation
SELECT
    DATE_FORMAT(month, '%Y-%m') AS period,
    'After Implementation' AS implementation_phase,
    SUM(estamps_challans_cnt) AS estamps_challans_count,
    SUM(documents_registered_cnt) AS documents_registered_count
FROM
    fact_stamps
WHERE
    month >= '2020-01-01'
GROUP BY
    DATE_FORMAT(month, '%Y-%m');




-- Categorize districts into three segments based on their stamp registration revenue generation during the fiscal year 2021 to 2022. 
 
SELECT
    dist_code,
    revenue_2021_2022,
    CASE
        WHEN revenue_quantile = 1 THEN 'Low Revenue'
        WHEN revenue_quantile = 2 THEN 'Medium Revenue'
        WHEN revenue_quantile = 3 THEN 'High Revenue'
    END AS revenue_segment
FROM (
    SELECT
        dist_code,
        revenue_2021_2022,
        NTILE(3) OVER (ORDER BY revenue_2021_2022) AS revenue_quantile
    FROM (
        SELECT
            dist_code,
            SUM(CASE
                WHEN (YEAR(month) = 2021 AND MONTH(month) >= 4) OR
                     (YEAR(month) = 2022 AND MONTH(month) <= 3) THEN documents_registered_rev
                ELSE 0
            END) AS revenue_2021_2022
        FROM
            fact_stamps
        GROUP BY
            dist_code
    ) AS Revenue2021_2022
) AS RevenueQuantiles;





-- Transport dataset --
-- Investigate whether there is any correlation between vehicle sales and specific months or seasons in different districts. Are there any months or seasons that consistently show higher or lower sales rate, (Consider Fuel-Type category only) 
SELECT
    month,
    SUM(fuel_type_petrol) AS petrol_sales,
    SUM(fuel_type_diesel) AS diesel_sales,
    SUM(fuel_type_electric) AS electric_sales,
    SUM(fuel_type_others) AS others_sales
FROM
    fact_transport
GROUP BY
    month
ORDER BY
    month;

-- total vehicle sale
SELECT
    month,
    (fuel_type_petrol + fuel_type_diesel + fuel_type_electric + fuel_type_others) AS total_vehicle_sales
FROM
    fact_transport
ORDER BY
    month;

-- How does the distribution of vehicles vary by vehicle class (MotorCycle, MotorCar, AutoRickshaw, Agriculture) across different districts? 
SELECT
    d.district AS district_name,
    t.vehicleClass_MotorCycle,
    t.vehicleClass_MotorCar,
    t.vehicleClass_AutoRickshaw,
    t.vehicleClass_Agriculture
FROM
    fact_transport t
JOIN
    district_names d ON t.dist_code = d.dist_code;


-- 7.	List down the top 3 and bottom 3 districts that have shown the highest and lowest vehicle sales growth during FY 2022 compared to FY 2021? (Consider and compare categories: Petrol, Diesel and Electric) 

SELECT
    v.dist_code,
    d.district,
    v.fuel_type,
    SUM(v.sales_growth) AS sales_growth
FROM
    (
    SELECT
        t.dist_code,
        t.month,
        'Petrol' AS fuel_type,
        SUM(t.fuel_type_petrol - lag_petrol) AS sales_growth
    FROM
        (
        SELECT
            t.*,
            LAG(t.fuel_type_petrol) OVER (PARTITION BY t.dist_code ORDER BY t.month) AS lag_petrol
        FROM
           fact_transport t
        WHERE
            EXTRACT(YEAR FROM t.month) = 2022
        ) t
    GROUP BY
        t.dist_code, t.month
    
    UNION ALL

    SELECT
        t.dist_code,
        t.month,
        'Diesel' AS fuel_type,
        SUM(t.fuel_type_diesel - lag_diesel) AS sales_growth
    FROM
        (
        SELECT
            t.*,
            LAG(t.fuel_type_diesel) OVER (PARTITION BY t.dist_code ORDER BY t.month) AS lag_diesel
        FROM
            fact_transport t
        WHERE
            EXTRACT(YEAR FROM t.month) = 2022
        ) t
    GROUP BY
        t.dist_code, t.month

    UNION ALL

    SELECT
        t.dist_code,
        t.month,
        'Electric' AS fuel_type,
        SUM(t.fuel_type_electric - lag_electric) AS sales_growth
    FROM
        (
        SELECT
            t.*,
            LAG(t.fuel_type_electric) OVER (PARTITION BY t.dist_code ORDER BY t.month) AS lag_electric
        FROM
            fact_transport t
        WHERE
            EXTRACT(YEAR FROM t.month) = 2022
        ) t
    GROUP BY
        t.dist_code, t.month
    ) v
JOIN
    district_names d ON v.dist_code = d.dist_code
GROUP BY
    v.dist_code,
    d.district,
    v.fuel_type
ORDER BY
    v.fuel_type,
    sales_growth DESC;


-- Ipass dataset
-- top 5 sectors with high investment--    
WITH FiscalYearFilter AS (
    SELECT 
        I.month,
        I.investment_in_cr AS investment_in_cr,
        I.sector,
        D.fiscal_year
    FROM 
        fact_ts_ipass I
    JOIN
        Date D ON DATE_FORMAT(STR_TO_DATE(I.month, '%d-%m-%Y'), '%Y-%m-%d') = D.month
        
    WHERE 
        D.fiscal_year = 2022
)
SELECT 
    sector,
    SUM(investment_in_cr) AS total_investment_in_cr
FROM 
    FiscalYearFilter
GROUP BY 
    sector
ORDER BY 
    total_investment_in_cr DESC
LIMIT 5; 



--  down the top 3 districts that have attracted the most significant sector investments during FY 2019 to 2022?
WITH FiscalYearFilter AS (
    SELECT
        I.dist_code,
        SUM(I.investment_in_cr) AS total_investment_in_cr
    FROM
        fact_ts_ipass AS I
    JOIN
        Date D ON DATE_FORMAT(STR_TO_DATE(I.month, '%d-%m-%Y'), '%Y-%m-%d') = D.month
    WHERE
        D.fiscal_year BETWEEN 2019 AND 2022
    GROUP BY
        I.dist_code
)

-- Join the filtered data with district names
SELECT
    DN.district,
    F.total_investment_in_cr
FROM
    district_names AS DN
JOIN
    FiscalYearFilter AS F ON DN.dist_code = F.dist_code
ORDER BY
    F.total_investment_in_cr DESC
LIMIT
    3;
    
    