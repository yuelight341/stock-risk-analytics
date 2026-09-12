SELECT
    ticker,
    ROUND(MAX((running_peak - close) / running_peak) * 100, 2) AS max_drawdown_pct
FROM memory.price_with_peak
GROUP BY ticker
ORDER BY max_drawdown_pct DESC;