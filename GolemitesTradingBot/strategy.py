# strategy.py
def simple_strategy(price):
    # VERY BASIC (we will improve later)
    if price > 50000:
        return "SELL"
    elif price < 40000:
        return "BUY"
    else:
        return "HOLD"