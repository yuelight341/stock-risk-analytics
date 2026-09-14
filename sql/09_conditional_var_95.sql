WITH var_threshold AS (
    SELECT
        ticker,
        QUANTILE_CONT(daily_return, 0.05) AS var_95
    FROM s.daily_prices
    WHERE daily_return IS NOT NULL
    GROUP BY ticker
)
SELECT
    p.ticker,
    ROUND(AVG(p.daily_return) * 100, 2) AS cvar_95_pct
FROM s.daily_prices p
JOIN var_threshold v USING (ticker)
WHERE p.daily_return IS NOT NULL
  AND p.daily_return <= v.var_95
GROUP BY p.ticker
ORDER BY cvar_95_pct ASC;
