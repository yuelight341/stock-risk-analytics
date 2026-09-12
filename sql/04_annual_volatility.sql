SELECT 
    ticker, 
    ROUND(STDDEV_SAMP(daily_return) * SQRT(252) * 100, 2) AS annual_volatility_pct
FROM s.daily_prices
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY annual_volatility_pct DESC;