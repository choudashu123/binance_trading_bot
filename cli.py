def get_user_input():
    print("==== Binance Futures Testnet Trading Bot")
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter side (buy/sell): ").lower()
    order_type = input("Enter order type (market/limit/stop_limit): ").lower()
    quantity = float(input("Enter quantity"))

    price = None
    stop_price = None
    if order_type == "limit" :
        price = float(input("Enter price: "))

    elif order_type == "stop_limit":
        stop_price = input("Enter stop price: ")
        price = input("Enter limit price: ")

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
        "stop_price": stop_price
    }