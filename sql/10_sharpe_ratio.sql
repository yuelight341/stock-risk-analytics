SELECT
    ticker,
    ROUND(
        AVG(daily_return) / NULLIF(STDDEV_SAMP(daily_return), 0) * SQRT(252),
        2
    ) AS sharpe_ratio
FROM s.daily_prices
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY sharpe_ratio DESC;