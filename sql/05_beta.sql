WITH paired AS (
    SELECT
        s.ticker,
        s.daily_return  AS y,
        m.daily_return  AS x
    FROM s.daily_prices s
    JOIN s.daily_prices m
      ON s.date = m.date
     AND m.is_benchmark = 1
    WHERE s.is_benchmark = 0
      AND s.daily_return IS NOT NULL
      AND m.daily_return IS NOT NULL
)
SELECT
    ticker,
    ROUND(REGR_SLOPE(y, x), 3) AS beta
FROM paired
GROUP BY ticker
ORDER BY beta DESC;