SELECT
    ticker,
    ROUND(QUANTILE_CONT(daily_return, 0.05) * 100, 2) AS var_95_pct
FROM s.daily_prices
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY var_95_pct ASC;