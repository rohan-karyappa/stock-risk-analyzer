from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.data_ingestion import fetch_stock_data
from src.feature_engineering import calculate_daily_returns, calculate_volatility, calculate_sharpe_ratio, calculate_max_drawdown
from src.risk_scorer import calculate_risk_score

app = FastAPI(title = 'Stock Risk Analyzer API')

class RiskReport(BaseModel):
    ticker: str
    period: str
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    risk_score: int
    risk_label: str

@app.get("/analyse", response_model=RiskReport)
def analyse_stock(ticker:str, period:str):
    try:
        #Step 1: Fetch Data
        df = fetch_stock_data(ticker, period)
        
        #Step 2: Calculate Features
        returns = calculate_daily_returns(df)
        vol = calculate_volatility(returns)
        sharpe = calculate_sharpe_ratio(returns, vol)
        drawdown = calculate_max_drawdown(returns)

        #Step 3: Score the Risk
        risk_result = calculate_risk_score(ticker, vol, sharpe, drawdown)

        #Step 4: Return the final JSON response
        return RiskReport(
            ticker=ticker,
            period=period,
            volatility=vol,
            sharpe_ratio=sharpe,
            max_drawdown=drawdown,

            risk_score=risk_result['risk_score'],
            risk_label=risk_result['risk_label']
        )
    
    except ValueError as ve:
        #Returns a clean 400 error if the user types a bad ticker
        raise HTTPException(status_code=400,detail=str(ve))
    
    except Exception as e:
        #Returns a 500 error if anything else breaks
        raise HTTPException(status_code=500,detail=f'Internal server error: {str(e)}')