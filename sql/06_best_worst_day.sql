WITH ranked AS (
    SELECT
        ticker,
        date,
        daily_return,
        RANK() OVER (PARTITION BY ticker ORDER BY daily_return DESC) AS best_rank,
        RANK() OVER (PARTITION BY ticker ORDER BY daily_return ASC)  AS worst_rank
    FROM s.daily_prices
    WHERE daily_return IS NOT NULL
)
SELECT
    ticker,
    MAX(CASE WHEN best_rank  = 1 THEN date END)                          AS best_day_date,
    ROUND(MAX(CASE WHEN best_rank  = 1 THEN daily_return END) * 100, 2)  AS best_day_pct,
    MAX(CASE WHEN worst_rank = 1 THEN date END)                          AS worst_day_date,
    ROUND(MAX(CASE WHEN worst_rank = 1 THEN daily_return END) * 100, 2)  AS worst_day_pct
FROM ranked
GROUP BY ticker
ORDER BY ticker;