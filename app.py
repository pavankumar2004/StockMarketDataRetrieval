from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from Trie import Trie
from RedBlackTree import RedBlackTree
import requests

app = Flask(__name__)


trie = Trie()
rbt = RedBlackTree()
app.secret_key="wxvUpvUtdBqH7UO"
ALPHA_VANTAGE_API_KEY = "IFK7UKQH1E5HGN2G"

# Function to load stock symbols into the Trie and Red-Black Tree
def load_stock_symbols():
    # Load stock symbols into the Trie and Red-Black Tree
    symbols = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG",  # Tech Giants
    "TSLA", "NVDA", "NFLX", "FB", "INTC",    # Tech and Electric Vehicles
    "JPM", "GS", "BAC", "C", "WFC",         # Banks
    "V", "MA", "AXP", "PYPL", "SQ",         # Payment and Finance
    "JNJ", "PFE", "MRK", "GSK", "AZN",     # Pharmaceuticals
    "WMT", "AMZN", "TGT", "COST", "HD",    # Retail
    "DIS", "CMCSA", "FOXA", "NFLX", "DISCA",# Entertainment
    "PG", "KO", "PEP", "PM", "MO",         # Consumer Goods
    "XOM", "CVX", "TOT", "RDS.A", "BP",    # Energy
    "T", "VZ", "TMUS", "S", "CHT",         # Telecommunications
    "CSCO", "IBM", "ORCL", "HPE", "AAP"    # Tech and Enterprise
]
    for symbol in symbols:
        trie.insert(symbol)

# Load stock symbols when the application starts
load_stock_symbols()
stock_data = []

@app.route("/", methods=["GET", "POST"])
def get_stock_data():
            symbol = request.form.get("symbol")
            if not symbol:
                return render_template("index.html", error="Please enter a valid stock symbol.")

            # Make an API request to Alpha Vantage
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url)
            data = response.json()

            # Check if the request was successful
            if "Time Series (5min)" in data:
                time_series = data["Time Series (5min)"]

                # Initialize a list to store the "low" values
                low = []
                timestamps = []
                low_values = []

                for timestamp, values in time_series.items():
                    # Extract and append the "low" value to the list
                    timestamps.append(timestamp)
                    low_value = float(values["3. low"])
                    low.append(low_value)

                # Append the low values and timestamps for this symbol to stock_data
                stock_data.append({
                    "symbol": symbol,
                    "timestamps": timestamps,
                    "low": low_values,
                })

                # Insert the symbol into the Red-Black Tree with the low values
                rbt.insert(symbol, low)
                for i in range(len(timestamps)):
                    timestamps[i] = timestamps[i][10:16]
                low_values = rbt.traverse() 
                low_values = low_values[0]
                print(low_values)# Assuming 'rbt' is an instance of RedBlackTree
                mindata = min(low_values)
                lowest = min(low_values)
                highest = max(low_values)
                for i in range(len(low)):
                    if low[i] == lowest:
                        timelow = timestamps[i]
                for i in range(len(low)):
                    if low[i] == highest:
                        timehigh = timestamps[i]

                return render_template('low_values.html', low_values=low_values, timestamps=timestamps, low=low, symbol=symbol,
                                       lowest=lowest, timelow=timelow, timehigh=timehigh, highest=highest)



# Auto-complete route to provide stock symbol suggestions
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '').upper()
    suggestions = trie.search(prefix)
    return jsonify(suggestions)



if __name__ == "__main__":
    app.run(debug=True)
                         