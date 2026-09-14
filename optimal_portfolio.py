import sqlite3
import pandas as pd
import scipy as sp
import numpy as np
from scipy.optimize import minimize

DB_PATH = "stock_data.db"
PORTFOLIO_TICKER = "O_PORTFOLIO"

def calculate_and_insert_portfolio():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT date, ticker, close FROM daily_prices WHERE is_benchmark = 0", conn)
    
    prices = df.pivot(index='date', columns='ticker', values='close')
    returns = prices.pct_change().dropna()
    
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    num_assets = len(returns.columns)
    
    def negative_sharpe(w):
        p_ret = np.sum(mean_returns * w)
        p_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        return -(p_ret / p_vol)
    
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets,]
    
    optimal = minimize(negative_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    weights = optimal.x
    
    weight_df = pd.DataFrame({'Ticker': returns.columns, 'Weight %': np.round(weights * 100, 2)})
    print("\n--- Optimal Tangency Portfolio Weights ---")
    print(weight_df.sort_values(by='Weight %', ascending=False).to_string(index=False))
    
    portfolio_daily_returns = returns.dot(weights)
    
    synthetic_prices = 100 * (1 + portfolio_daily_returns).cumprod()
    
    port_df = pd.DataFrame({
        'date': portfolio_daily_returns.index,
        'ticker': PORTFOLIO_TICKER,
        'close': synthetic_prices,
        'is_benchmark': 0
    })
    
    port_df['daily_return'] = portfolio_daily_returns.values
    port_df['sma_50d'] = port_df['close'].rolling(50).mean()
    port_df['vol_30d'] = port_df['daily_return'].rolling(30).std() * np.sqrt(252)
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(f"DELETE FROM daily_prices WHERE ticker = '{PORTFOLIO_TICKER}'")
        
        port_df.to_sql("daily_prices", conn, if_exists="append", index=False)
        
    print(f"\n'{PORTFOLIO_TICKER}' has been added to the database.")

if __name__ == "__main__":
    calculate_and_insert_portfolio()
