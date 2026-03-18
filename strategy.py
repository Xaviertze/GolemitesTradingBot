# strategy.py
'''
last_price = None

def simple_strategy(current_price):
    global last_price

    if last_price is None:
        last_price = current_price
        return "HOLD"

    if current_price < last_price * 0.999:
        signal = "BUY"
    elif current_price > last_price * 1.001:
        signal = "SELL"
    else:
        signal = "HOLD"

    last_price = current_price
    return signal
'''
prices = []

def simple_strategy(current_price):
    prices.append(current_price)

    if len(prices) < 5:
        return "HOLD"

    short_avg = sum(prices[-3:]) / 3
    long_avg = sum(prices[-5:]) / 5

    if short_avg > long_avg:
        return "BUY"
    elif short_avg < long_avg:
        return "SELL"
    else:
        return "HOLD"