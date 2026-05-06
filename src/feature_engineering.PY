import numpy as np
import pandas as pd
from .utils import get_logger

logger = get_logger(__name__)

def calculate_daily_returns(df):
    # This calculates the percentage change from the previous day's close
    logger.info("Calculating daily returns")
    df['Daily_Return']=df['Close'].pct_change()
    df.iloc[0,df.columns.get_loc('Daily_Return')]=0
    returns = df['Daily_Return']
    return returns

def calculate_volatility(returns):
    # std() gets the daily volatility. We multiply by sqrt(252) to annualise it (252 trading days in a year)
    logger.info("Calculating annualised volatility")
    volatility = returns.std() * np.sqrt(252)
    return volatility

def calculate_sharpe_ratio(returns, volatility):
    mean_return = returns.mean()
    sharpe_ratio = (mean_return*252)/volatility
    return sharpe_ratio

def calculate_max_drawdown(returns):
    # First, we calculate the cumulative return over time (if you invested $1, what is it worth now?)
    # Then we find the biggest drop from an all-time high
    logger.info('Calculating Max Drawdowns')
    cumulative_return = (1+returns).cumprod()
    max_drawdown = (cumulative_return / cumulative_return.cummax() - 1).min()
    return max_drawdown

