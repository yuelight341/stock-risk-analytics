SELECT 
    ticker,
    ROUND(
        (POWER(
            ARG_MAX(close, date) / ARG_MIN(close, date), 
            252.0 / COUNT(date)
        ) - 1) * 100, 
    2) AS annualized_return_pct
FROM s.daily_prices
GROUP BY ticker
ORDER BY annualized_return_pct DESC;