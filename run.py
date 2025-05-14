from logger import setup_logger
from bot import BasicBot
from cli import get_user_input
from binance.enums import *
import os

ORDER_TYPE_MAP = {
    "market": "MARKET",
    "limit": "LIMIT",
    "stop_limit": "STOP_LIMIT"
}

def main():
    setup_logger()
    bot = BasicBot(os.environ.get("API_KEY"), os.environ.get("API_SECRET"), testnet=True)

    user_input = get_user_input()
    symbol = user_input["symbol"]
    side = user_input["side"]
    order_type_key = user_input['order_type'].lower()

    order_type = ORDER_TYPE_MAP.get(order_type_key)
    if not order_type:
        print("❌ Invalid order type.")
        return
    quantity = user_input["quantity"]
    price = user_input.get("price")
    stop_price = user_input.get("stop_price")

    result = bot.place_order(
        symbol, 
        side, 
        order_type, 
        quantity, 
        price, 
        stop_price
        )

    if result:
        print("✅ Order placed successfully!")
        print(result)
    else:
        print("❌ Failed to place order.")

if __name__ == "__main__":
    main()