from .utils import get_logger

logger = get_logger(__name__)

def calculate_risk_score(stock_ticker, volatility, sharpe_ratio, max_drawdown):
    logger.info('Calculating the risk score')
    risk_score=0

    # 1. Score Volatility (Max 33 points)
    if volatility > 0.40:
        risk_score+=33
    elif volatility >=0.20:
        risk_score+=16
    else:
        risk_score+=0

    # 2. Score Sharpe Ratio (Max 33 points)
    # Note: A lower Sharpe Ratio is MORE risky
    if sharpe_ratio<0:
        risk_score+=33
    elif sharpe_ratio<1.0:
        risk_score+=16
    else:
        risk_score+=0
    
    # 3. Score Max Drawdown (Max 34 points)
    # Note: A lower drawdown (like -0.40) is MORE risky

    if max_drawdown < -0.30:
        risk_score+=34
    elif max_drawdown < -0.15:
        risk_score+=16
    else:
        risk_score+=0

    risk_label=''
    
    if risk_score >= 70:
        risk_label='High'
    elif risk_score >= 30:
        risk_label='Medium'
    else:
        risk_label='Low'

    logger.info(f'Assigned label "{risk_label}" for the stock "{stock_ticker}" with score {risk_score} ')

    # Return a dictionary so it's easy to pass to our API later!

    return {
        'risk_score' : risk_score,
        'risk_label' : risk_label
    }

    