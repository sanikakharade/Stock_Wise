# StockWise
A Django backend system that fetches financial data from a public API, stores it in a relational database, implements a basic backtesting module using this historical data, and generates reports with performance results.


# 1. Retrieve all stock prices
curl -X GET http://127.0.0.1:8000/api/v1/stock-prices/

# 2. Retrieve stock prices for a specific symbol
curl -X GET http://127.0.0.1:8000/api/v1/stock-prices/AAPL/

# 3. Fetch and store stock data for a specific symbol
curl -X POST http://127.0.0.1:8000/api/v1/stock-prices/fetch/AAPL/ \
-H "Content-Type: application/json"

# 4. Backtest on historical stock prices
curl -X POST http://127.0.0.1:8000/api/v1/backtest/ \
-H "Content-Type: application/json" \
-d '{"symbol": "AAPL", "initial_investment": 10000.00}'

# 5. Predict future stock prices.
curl -X POST http://127.0.0.1:8000/api/v1/prediction/AAPL/ \
-H "Content-Type: application/json"

# 6. Generate Report
curl -X POST http://localhost:8000/api/v1/report/ \
-H "Content-Type: application/json" \
-d '{ 
    "symbol": "AAPL",
    "format": "pdf",
    "initial_investment": 10000.00
}' --output AAPL_report.pdf


