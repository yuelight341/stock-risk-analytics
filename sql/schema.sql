daily_prices (
    date         DATE,
    ticker       VARCHAR,
    open         DOUBLE,
    high         DOUBLE,
    low          DOUBLE,
    close        DOUBLE,
    volume       BIGINT,
    daily_return DOUBLE,
    sma_50d      DOUBLE,
    vol_30d      DOUBLE,
    PRIMARY KEY (ticker, date)
)