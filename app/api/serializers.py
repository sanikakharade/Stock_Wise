from rest_framework import serializers
from app.core.models import StockPrice, StockPrediction

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['symbol', 'timestamp', 'open', 'close', 'high', 'low', 'volume']

    def validate_timestamp(self, value):
        if StockPrice.objects.filter(symbol=self.initial_data['symbol'], timestamp=value).exists():
            raise serializers.ValidationError("A stock price entry for this symbol and timestamp already exists.")
        return value

class BacktestSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    initial_investment = serializers.DecimalField(max_digits=10, decimal_places=2)
    
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrediction
        fields = ['symbol', 'prediction_date', 'predicted_price']
    