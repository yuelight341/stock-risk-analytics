WITH paired AS (
    SELECT
        s.ticker,
        s.date,
        s.daily_return       AS stock_return,
        m.daily_return       AS market_return
    FROM s.daily_prices s
    JOIN s.daily_prices m
      ON s.date = m.date
     AND m.is_benchmark = 1
    WHERE s.is_benchmark = 0
      AND s.daily_return IS NOT NULL
      AND m.daily_return IS NOT NULL
)
SELECT
    ticker,
    ROUND(REGR_INTERCEPT(stock_return, market_return) * 252 * 100, 2) AS alpha_annualized_pct
FROM paired
GROUP BY ticker
ORDER BY alpha_annualized_pct DESC;