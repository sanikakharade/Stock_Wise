import matplotlib.pyplot as plt
import io
import base64

def generate_stock_price_history_chart(historical_data):
    plt.figure(figsize=(10, 6))
    dates = [data['timestamp'] for data in historical_data]
    prices = [data['close'] for data in historical_data]
    plt.plot(dates, prices, label='Stock Price History')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Historical Stock Prices')
    plt.legend()
    return get_image_as_base64()

def generate_prediction_vs_actual_chart(predictions, actual_prices):
    plt.figure(figsize=(10, 6))
    dates = [pred['prediction_date'] for pred in predictions]
    predicted_prices = [pred['predicted_price'] for pred in predictions]
    actuals = [actual['close'] for actual in actual_prices]
    plt.plot(dates, predicted_prices, label='Predicted Prices', linestyle='--')
    plt.plot(dates, actuals[-30:], label='Actual Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Predicted vs Actual Stock Prices')
    plt.legend()
    return get_image_as_base64()

def get_image_as_base64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')
