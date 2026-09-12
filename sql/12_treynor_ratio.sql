WITH ret AS (
    SELECT 
        ticker,
        (POWER(ARG_MAX(close, date) / ARG_MIN(close, date), 252.0 / COUNT(date)) - 1) * 100 AS annualized_return_pct
    FROM s.daily_prices
    WHERE is_benchmark = 0
    GROUP BY ticker
),
beta_calc AS (
    SELECT
        s.ticker,
        REGR_SLOPE(s.daily_return, m.daily_return) AS beta
    FROM s.daily_prices s
    JOIN s.daily_prices m
      ON s.date = m.date
     AND m.is_benchmark = 1
    WHERE s.is_benchmark = 0
      AND s.daily_return IS NOT NULL
      AND m.daily_return IS NOT NULL
    GROUP BY s.ticker
)
SELECT
    r.ticker,
    ROUND(r.annualized_return_pct / b.beta, 2) AS treynor_ratio
FROM ret r
JOIN beta_calc b ON r.ticker = b.ticker
ORDER BY treynor_ratio DESC;