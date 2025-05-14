from flask import Flask, render_template, request, redirect, url_for, flash
from bot import BasicBot
from logger import setup_logger
import os

setup_logger()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
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
        if result :
            flash(f"✅ Order placed successfully!\n{result}", "success")
        else :
            flash("❌ Failed to place order.", "danger")
        
        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
