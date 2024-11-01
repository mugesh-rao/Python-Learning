from flask import Flask, render_template_string, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to fetch stock information
def fetch_stock_info(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol + ".NS")
        date_intervals = [1, 2, 7, 10, 30]
        percentage_returns = {}

        for days in date_intervals:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            historical_data = stock.history(start=start_date, end=end_date)
            start_price = historical_data.iloc[0]['Close']
            end_price = historical_data.iloc[-1]['Close']
            percentage_return = ((end_price - start_price) / start_price) * 100
            percentage_returns[f"{days} Days"] = round(percentage_return, 2)

        return {"Symbol": stock_symbol, **percentage_returns}

    except Exception as e:
        return {"Error": str(e)}

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    stock_symbol = request.form['stock_symbol']
    stock_info = fetch_stock_info(stock_symbol)
    return jsonify(stock_info)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Market Prediction</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7fa; }
        .card { background: #fff; border-radius: 8px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); }
        .button { background-color: #ff5a5f; color: #fff; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <div class="text-center">
            <h1 class="text-3xl font-bold mb-8 text-gray-800">📈 Stock Market Prediction</h1>
        </div>
        <div class="max-w-md mx-auto card p-6">
            <form id="stockForm" class="space-y-4">
                <label for="stockSymbol" class="block text-lg font-medium text-gray-700">Enter Indian Stock Symbol (e.g., TATAMOTORS):</label>
                <input type="text" id="stockSymbol" name="stock_symbol" required class="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-400 focus:outline-none">
                <button type="submit" class="w-full p-3 button rounded-md hover:bg-red-600 transition duration-200">Predict</button>
            </form>
            <div class="result mt-8" id="result"></div>
        </div>
    </div>

    <script>
        document.getElementById('stockForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const stockSymbol = document.getElementById('stockSymbol').value;
            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'stock_symbol=' + stockSymbol
            })
            .then(response => response.json())
            .then(data => {
                let output = '<div class="mt-4 p-4 rounded-md bg-gray-100">';
                if (data.Error) {
                    output += `<p class="text-red-500 font-bold">Error: ${data.Error}</p>`;
                } else {
                    output += `<p class="text-lg font-semibold text-gray-700">Symbol: <span class="text-blue-500">${data.Symbol}</span></p>`;
                    output += `<p class="text-gray-600">Percentage Return (1 Day): ${data["1 Days"]}%</p>`;
                    output += `<p class="text-gray-600">Percentage Return (2 Days): ${data["2 Days"]}%</p>`;
                    output += `<p class="text-gray-600">Percentage Return (1 Week): ${data["7 Days"]}%</p>`;
                    output += `<p class="text-gray-600">Percentage Return (10 Days): ${data["10 Days"]}%</p>`;
                    output += `<p class="text-gray-600">Percentage Return (1 Month): ${data["30 Days"]}%</p>`;
                }
                output += '</div>';
                document.getElementById('result').innerHTML = output;
            })
            .catch(error => console.error('Error:', error));
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
