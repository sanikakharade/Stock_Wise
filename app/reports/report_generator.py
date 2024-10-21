from django.template.loader import render_to_string
from .visualizations import generate_stock_price_history_chart, generate_prediction_vs_actual_chart
from weasyprint import HTML
from io import BytesIO

def generate_report(symbol, historical_data, predictions, backtest_data):
    
    report_template = "../templates/reports/report_template.html"
    
    history_chart = generate_stock_price_history_chart(historical_data)
    prediction_chart = generate_prediction_vs_actual_chart(predictions, historical_data)
    
    json_report = {
        "symbol": symbol,
        "historical_data": historical_data,
        "predictions": predictions,
        "backtest": backtest_data,
        "charts": {
            "history_chart": history_chart,
            "prediction_vs_actual_chart": prediction_chart,
        }
    }
    
    html_report = render_to_string(report_template, {
        "symbol": symbol,
        "historical_data": historical_data,
        "predictions": predictions,
        "backtest": backtest_data,
        "history_chart": history_chart,
        "prediction_vs_actual_chart": prediction_chart
    })
    
    pdf_output = BytesIO()
    HTML(string=html_report).write_pdf(pdf_output)
    pdf_output.seek(0)

    return json_report, html_report, pdf_output
