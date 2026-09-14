import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "stock_data.db"
RESULTS_DIR = Path("output/results")
GRAPHS_DIR = Path("output/graphs")

sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (12, 7)

def get_timeseries_data():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT date, ticker, close, daily_return, is_benchmark FROM daily_prices", conn)
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_wealth_index(df, benchmark_ticker):
    prices = df.pivot(index='date', columns='ticker', values='close').dropna()
    wealth = (prices / prices.iloc[0]) * 100
    
    plt.figure()
    for col in wealth.columns:
        if col == 'O_PORTFOLIO':
            plt.plot(wealth.index, wealth[col], label='O_PORTFOLIO', linewidth=3, color='crimson')
        elif col == benchmark_ticker:
            plt.plot(wealth.index, wealth[col], label=f'{benchmark_ticker}', linewidth=2, color='black', linestyle='--')
        else:
            plt.plot(wealth.index, wealth[col], label=col, linewidth=1.5, alpha=0.5)
            
    plt.title("Wealth Index (Cumulative Growth of $100)")
    plt.ylabel("Value ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / "01_wealth_index.png")
    plt.close()

def plot_underwater(df, benchmark_ticker):
    prices = df.pivot(index='date', columns='ticker', values='close').dropna()
    
    port_rolling_max = prices['O_PORTFOLIO'].cummax()
    port_drawdown = (prices['O_PORTFOLIO'] - port_rolling_max) / port_rolling_max * 100
    
    bm_rolling_max = prices[benchmark_ticker].cummax()
    bm_drawdown = (prices[benchmark_ticker] - bm_rolling_max) / bm_rolling_max * 100
    
    plt.figure()
    plt.fill_between(port_drawdown.index, port_drawdown, 0, color='crimson', alpha=0.3, label='O_PORTFOLIO')
    plt.plot(bm_drawdown.index, bm_drawdown, color='black', linewidth=1, linestyle='--', label=f'{benchmark_ticker}')    
    plt.title("Underwater Plot (Historical Drawdowns)")
    plt.ylabel("Drawdown (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / "02_underwater_plot.png")
    plt.close()

def plot_tail_risk(df):
    port_returns = df[df['ticker'] == 'O_PORTFOLIO']['daily_return'].dropna()
    
    var_95 = np.percentile(port_returns, 5)
    cvar_95 = port_returns[port_returns <= var_95].mean()
    
    plt.figure()
    sns.histplot(port_returns * 100, bins=100, kde=True, color='steelblue')
    
    plt.axvline(var_95 * 100, color='orange', linestyle='dashed', linewidth=2, label=f'95% VaR: {var_95*100:.2f}%')
    plt.axvline(cvar_95 * 100, color='red', linestyle='dashed', linewidth=2, label=f'95% CVaR: {cvar_95*100:.2f}%')
    
    plt.title("Portfolio Daily Returns Distribution (Tail Risk)")
    plt.xlabel("Daily Return (%)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / "03_tail_risk.png")
    plt.close()

def plot_risk_reward():
    try:
        ret = pd.read_csv(RESULTS_DIR / "01_annualized_return.csv")
        vol = pd.read_csv(RESULTS_DIR / "04_annual_volatility.csv")
        df = pd.merge(ret, vol, on='ticker')
        
        plt.figure()
        sns.scatterplot(data=df, x='annual_volatility_pct', y='annualized_return_pct', s=150, hue='ticker', legend=False)
        
        for i in range(df.shape[0]):
            plt.text(x=df.annual_volatility_pct[i] + 0.05, 
                     y=df.annualized_return_pct[i], 
                     s=df.ticker[i], 
                     fontdict=dict(color='black', size=10))
            
        plt.title("Risk vs. Reward (Annualized)")
        plt.xlabel("Annual Volatility (%)")
        plt.ylabel("Annualized Return (%)")
        plt.tight_layout()
        plt.savefig(GRAPHS_DIR / "04_risk_reward.png")
        plt.close()
    except FileNotFoundError:
        print("[WARNING] Could not find return/volatility CSVs. Run run_queries.py first.")

def main():
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    df = get_timeseries_data()
    
    benchmark_rows = df[df['is_benchmark'] == 1]
    if not benchmark_rows.empty:
        benchmark_ticker = benchmark_rows['ticker'].iloc[0]
        print(f"Detected Benchmark: {benchmark_ticker}")
    else:
        print("[WARNING] No benchmark found in database. Defaulting to ^GSPC")
        benchmark_ticker = "^GSPC"
    
    plot_wealth_index(df, benchmark_ticker)
    
    plot_underwater(df, benchmark_ticker)
    
    plot_tail_risk(df)
    
    plot_risk_reward()
    
    print(f"\nAll graphs saved to {GRAPHS_DIR.absolute()}")

if __name__ == "__main__":
    main()
