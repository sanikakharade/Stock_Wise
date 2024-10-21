from django.test import TestCase
from app.core.models import StockPrice
from app.core.services import backtest_strategy
import pandas as pd

class BacktestTest(TestCase):
    def setUp(self):
        data = {
            'timestamp': pd.date_range(start='2020-01-01', periods=300),
            'close': [100 + (i % 10) for i in range(300)]
        }
        df = pd.DataFrame(data)
        for _, row in df.iterrows():
            StockPrice.objects.create(timestamp=row['timestamp'], close=row['close'], symbol='AAPL')

    def test_backtest(self):
        stock_data = StockPrice.objects.filter(symbol='AAPL').order_by('timestamp')
        df = pd.DataFrame(list(stock_data.values('timestamp', 'close')))
        df.set_index('timestamp', inplace=True)

        result = backtest_strategy(df, initial_investment=10000)
        
        self.assertIn('total_return', result)
        self.assertIn('max_drawdown', result)
        self.assertIn('number_of_trades', result)
