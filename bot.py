from binance.um_futures import UMFutures
import logging
import traceback



class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
            base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
            self.client = UMFutures(key=api_key, secret=api_secret, base_url=base_url)

    def place_order(self, symbol, side, order_type, quantity, price= None, stop_price=None):
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
            logging.info(f"placing order QUANTITY: {quantity}")
            return order
        except Exception as e:
            logging.error(f"Error placing order:  {e}")
            logging.error(traceback.format_exc())
            return None