CREATE OR REPLACE VIEW price_with_peak AS
SELECT
    ticker,
    date,
    close,
    MAX(close) OVER (
        PARTITION BY ticker
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_peak,
    LAG(close) OVER (
        PARTITION BY ticker ORDER BY date
    ) AS prev_close
FROM s.daily_prices;