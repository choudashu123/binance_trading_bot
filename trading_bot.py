from flask import Flask, render_template_string, request, redirect, url_for, flash
from binance.um_futures import UMFutures
import os
import logging
import traceback

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Setup basic bot class
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        self.client = UMFutures(key=api_key, secret=api_secret, base_url=base_url)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            print("Getting Balance")
            balance = self.client.balance()
            for b in balance:
                if b['asset'] == 'USDT':
                    print("USDT Balance:", b['balance'])
            params = {
                "symbol": symbol,
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity
            }

            if order_type.lower() == "limit":
                params["price"] = price
                params["timeInForce"] = "GTC"
            
            elif order_type.lower() == "stop_limit":
                params["type"] = 'STOP'
                params["price"] = price
                params["stopPrice"] = stop_price
                params["timeInForce"] = "GTC"

            logging.info(f"Placing Order: {params}")
            order = self.client.new_order(**params)
            logging.info(f"Order placed successfully: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            logging.error(traceback.format_exc())
            return None

# Set up logger
logging.basicConfig(level=logging.INFO)

# Initialize bot with API keys
bot = BasicBot(os.environ.get('API_KEY'), os.environ.get('API_SECRET'), testnet=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        side = request.form["side"]
        order_type = request.form["order_type"]
        quantity = float(request.form["quantity"])
        price = request.form.get("price", None)
        stop_price = request.form.get("stop_price", None)

        # Convert to float only if present
        if price: price = float(price)
        if stop_price: stop_price = float(stop_price)

        result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
        if result:
            flash(f"✅ Order placed successfully!\n{result}", "success")
        else:
            flash("❌ Failed to place order.", "danger")
        
        return redirect(url_for("index"))

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Binance Trading Bot</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="p-4">
    <div class="container">
        <h1>📈 Binance Futures Testnet Trading Bot</h1>
        <form method="POST">
            <div class="mb-3">
                <label>Symbol</label>
                <input type="text" name="symbol" class="form-control" required placeholder="e.g. BTCUSDT">
            </div>
            <div class="mb-3">
                <label>Side</label>
                <select name="side" class="form-control">
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                </select>
            </div>
            <div class="mb-3">
                <label>Order Type</label>
                <select name="order_type" class="form-control" onchange="toggleFields(this.value)">
                    <option value="MARKET">Market</option>
                    <option value="LIMIT">Limit</option>
                    <option value="STOP_LIMIT">Stop-Limit</option>
                </select>
            </div>
            <div class="mb-3">
                <label>Quantity</label>
                <input type="number" step="0.01" name="quantity" class="form-control" required>
            </div>
            <div class="mb-3" id="price-field" style="display:none;">
                <label>Price</label>
                <input type="number" step="0.01" name="price" class="form-control">
            </div>
            <div class="mb-3" id="stop-price-field" style="display:none;">
                <label>Stop Price</label>
                <input type="number" step="0.01" name="stop_price" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Place Order</button>
        </form>

        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }} mt-4 shadow rounded">
            <pre class="mb-0">{{ message }}</pre>
        </div>
        {% endfor %}
        {% endif %}
        {% endwith %}

    </div>

    <script>
        function toggleFields(type) {
            document.getElementById("price-field").style.display = (type === "LIMIT" || type === "STOP_LIMIT") ? "block" : "none";
            document.getElementById("stop-price-field").style.display = (type === "STOP_LIMIT") ? "block" : "none";
        }
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
