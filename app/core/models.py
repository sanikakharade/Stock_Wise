from django.db import models

class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    volume = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'timestamp']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['symbol', 'timestamp'], name='unique_stock_price')
        ]

    def __str__(self):
        return f"{self.symbol} - {self.timestamp}"

class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    prediction_date = models.DateField()

    def __str__(self):
        return f"Prediction for {self.symbol} on {self.prediction_date}: {self.predicted_price}"

class StockReport(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    report_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report for {self.symbol} - {self.created_at}"
