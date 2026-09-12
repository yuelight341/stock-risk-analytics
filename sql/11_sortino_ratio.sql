SELECT
    ticker,
    ROUND(
        AVG(daily_return)
        / NULLIF(STDDEV_SAMP(daily_return) FILTER (WHERE daily_return < 0), 0)
        * SQRT(252),
        2
    ) AS sortino_ratio
FROM s.daily_prices
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY sortino_ratio DESC;