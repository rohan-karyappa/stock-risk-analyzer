import yfinance as yf
import pandas as pd
from .utils import get_logger

logger = get_logger(__name__)

def fetch_stock_data(ticker, period):
    logger.info(f'Fetching data for {ticker} over the period of {period}')
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            raise ValueError(f'No data found for ticker : {ticker}')

        df = df[['Open','Close','Low','High']]
        logger.info(f'Successfully fetched {len(df)} rows for {ticker}')

        return df
    
    except Exception as e:
        logger.error(f'Failed to fetch {ticker}: {e}')
        raise

    