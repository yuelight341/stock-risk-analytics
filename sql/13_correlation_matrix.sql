WITH assets AS (
    SELECT ticker, date, daily_return
    FROM s.daily_prices
    WHERE is_benchmark = 0 
       AND ticker <> '_PORTFOLIO'
       AND daily_return IS NOT NULL
)
SELECT 
    a1.ticker AS ticker_a,
    a2.ticker AS ticker_b,
    ROUND(CORR(a1.daily_return, a2.daily_return), 3) AS correlation
FROM assets a1
JOIN assets a2 
    ON a1.date = a2.date
WHERE a1.ticker < a2.ticker 
GROUP BY a1.ticker, a2.ticker
ORDER BY a1.ticker, correlation DESC;