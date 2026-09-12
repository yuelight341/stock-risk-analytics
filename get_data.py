import sys
import sqlite3
import argparse
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np

DB_PATH = "stock_data.db"

def download(tickers, start, end):
    data = yf.download(
        tickers, start=start, end=end, auto_adjust=True, progress=False
    )
    if data.empty:
        raise ValueError(f"yfinance returned no data for {tickers}")
    return data

def to_long_df(data):
    df = data.stack(level=1).reset_index()
    df.columns = [c.lower() for c in df.columns]
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)

def add_features(df, benchmark):
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    df["sma_50d"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(50).mean()
    )
    df["vol_30d"] = df.groupby("ticker")["daily_return"].transform(
        lambda x: x.rolling(30).std() * np.sqrt(252)
    )
    
    df["is_benchmark"] = (df["ticker"] == benchmark).astype(int)
    
    return df

def save(df, path=DB_PATH):
    with sqlite3.connect(path) as conn:
        df.to_sql("daily_prices", conn, if_exists="replace", index=False)
    df.to_csv("stock_data.csv", index=False)

def main(tickers, benchmark, start, end):
    all_tickers = sorted(set(tickers) | {benchmark})
    raw = download(all_tickers, start, end)
    df = add_features(to_long_df(raw), benchmark)
    save(df)
    print(f"Saved {len(df):,} rows across {df['ticker'].nunique()} tickers from {start} to {end}")
    print(f"Benchmark {benchmark} included and flagged.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download stock and benchmark data")
    
    today = datetime.today()
    default_end = today.strftime('%Y-%m-%d')
    
    try:
        start_date_obj = today.replace(year=today.year - 15)
    except ValueError:
        start_date_obj = today.replace(year=today.year - 15, day=28)
        
    default_start = start_date_obj.strftime('%Y-%m-%d')

    parser.add_argument("tickers", nargs="*", default=["AAPL", "MSFT"], 
                        help="List of stock tickers separated by spaces")
    parser.add_argument("-b", "--benchmark", default="^GSPC", 
                        help="Benchmark ticker (default: ^GSPC)")
    parser.add_argument("-s", "--start", default=default_start,
                        help=f"Start date (YYYY-MM-DD). Default: {default_start} (15 years ago)")
    parser.add_argument("-e", "--end", default=default_end,
                        help=f"End date (YYYY-MM-DD). Default: {default_end} (Today)")
    
    args = parser.parse_args()
    
    total_tickers = set(args.tickers) | {args.benchmark}
    if len(total_tickers) < 2:
        print("Error: Please provide at least one distinct stock ticker alongside the benchmark.")
        sys.exit(1)
        
    main(args.tickers, args.benchmark, args.start, args.end)