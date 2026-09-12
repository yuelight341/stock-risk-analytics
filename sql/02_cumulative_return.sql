SELECT
    ticker,
    ROUND(
        (ARG_MAX(close, date) - ARG_MIN(close, date))
        / ARG_MIN(close, date) * 100, 2
    ) AS total_return_pct
FROM s.daily_prices
GROUP BY ticker
ORDER BY total_return_pct DESC;