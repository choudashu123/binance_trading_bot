from binance.client import Client
from binance.enums import *
import logging

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        self.client.API_URL = self.client.FUTURES_URL

    def place_order(self, symbol, side, order_type, quantity, price= None):
        try:
            params = {
                "symbol": symbol,
                "side": SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == ORDER_TYPE_LIMIT:
                params["price"] = price
                params["timeInForce"] = TIME_IN_FORCE_GTC

            logging.info(f"Placing Order: {params}")
            order = self.client.futures_create_order(**params)
            logging.info(f"Order placed successfully: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing order:  {e}")
            return None