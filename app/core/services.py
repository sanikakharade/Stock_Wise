import httpx
import pandas as pd
from .utils import load_model
import numpy as np
from datetime import datetime, timedelta
from django.conf import settings
from app.api.serializers import StockPriceSerializer
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = 'app/core/ml/model.pkl'
model = load_model(MODEL_PATH)

def fetch_stock_data(symbol):
    API_KEY = settings.ALPHA_VANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full'

    logger.info(f"Fetching stock data for symbol: {symbol}")
    
    with httpx.Client() as client:
        try:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            time_series = data.get('Time Series (Daily)', {})
            
            two_years_ago = datetime.now() - timedelta(days=2 * 365)
            for date, stats in time_series.items():
                if datetime.strptime(date, '%Y-%m-%d') >= two_years_ago:
                    stock_price_data = {
                        'symbol': symbol,
                        'timestamp': date,
                        'open': stats['1. open'],
                        'close': stats['4. close'],
                        'high': stats['2. high'],
                        'low': stats['3. low'],
                        'volume': stats['5. volume'],
                    }

                    serializer = StockPriceSerializer(data=stock_price_data)
                    if serializer.is_valid():
                        serializer.save()
                        logger.info(f"Stored stock data for {symbol} on {date}")
                    else:
                        logger.warning(f"Validation error for {symbol} on {date}: {serializer.errors}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching data for {symbol}: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {symbol}: {str(e)}")   
            
def calculate_moving_averages(prices):
    prices['50_MA'] = prices['close'].rolling(window=50).mean()
    prices['200_MA'] = prices['close'].rolling(window=200).mean()
    
    return prices

def backtest_strategy(prices, initial_investment):
    cash = initial_investment
    shares = 0
    total_return = 0
    max_drawdown = 0
    max_value = initial_investment
    trades = 0

    prices = calculate_moving_averages(prices)

    for _, row in prices.iterrows():
        close_price = row['close']
        moving_average_50 = row['50_MA']
        moving_average_200 = row['200_MA']

        if pd.notna(close_price) and pd.notna(moving_average_50) and pd.notna(moving_average_200):
            if close_price < moving_average_50 and shares == 0:  # Buy stock
                shares = cash / close_price
                cash = 0
                trades += 1
            elif close_price > moving_average_200 and shares > 0:  # Sell stock
                cash = shares * close_price
                shares = 0
                trades += 1

                portfolio_value = cash
                total_return = (portfolio_value - initial_investment) / initial_investment * 100
                max_value = max(max_value, portfolio_value)
                drawdown = (max_value - portfolio_value) / max_value * 100
                max_drawdown = max(max_drawdown, drawdown)

    return {
        'total_return_percentage': total_return,
        'max_drawdown_percentage': max_drawdown,
        'number_of_trades': trades,
        'final_cash': cash
    }
    
def predict_stock_prices(stock_data, days=30):
    last_prediction = stock_data['close'].iloc[-1]
    predictions = []
    for _ in range(days):
        next_prediction = model.predict(np.array([[last_prediction]]))[0]
        predictions.append(next_prediction)
        last_prediction = next_prediction

    return pd.DataFrame({
        'predicted_price': predictions,
        'date': pd.date_range(start=pd.Timestamp.now(), periods=days)
    })
