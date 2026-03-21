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

prices = []
position = None  # None or "HOLDING"
entry_price = None

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

def simple_strategy2(current_price):
    global prices, position, entry_price

    prices.append(current_price)

    # Need enough data
    if len(prices) < 10:
        return "HOLD"

    # Moving averages
    short_ma = sum(prices[-3:]) / 3
    long_ma = sum(prices[-8:]) / 8

    print(f"Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")

    # ?? BUY condition
    if short_ma > long_ma and position is None:
        position = "HOLDING"
        entry_price = current_price
        return "BUY"

    # ?? SELL condition (only if holding)
    elif short_ma < long_ma and position == "HOLDING":
        # optional: only sell if profitable
        if current_price > entry_price:
            position = None
            return "SELL"

    return "HOLD"



import statistics
import csv

prices = []
position = 0        # 1 = long, -1 = short (we only use 1 / 0 here)
entry_price = None
equity_peak = 0
equity = 100000     # simulated equity (you can improve later)

k = 0.001  # position sizing constant

def load_prices_from_csv(filename="price_log.csv"):
    global prices

    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header

            for row in reader:
                price = float(row[2])  # 3rd column = price
                prices.append(price)

        print(f"Loaded {len(prices)} historical prices")

    except FileNotFoundError:
        print("No price_log.csv found, starting fresh")


def moving_average(data, window):
    if len(data) < window:
        return None
    return sum(data[-window:]) / window


def compute_volatility(data, window=20):
    if len(data) < window:
        return None
    return statistics.stdev(data[-window:])


def yow_strategy(current_price):
    global prices, position, entry_price, equity, equity_peak

    prices.append(current_price)

    # Need enough data
    if len(prices) < 50:
        return "HOLD", 0

    # --- Indicators ---
    ma10 = moving_average(prices, 10)
    ma50 = moving_average(prices, 50)
    ma20 = moving_average(prices, 20)
    vol = compute_volatility(prices, 20)

    if not all([ma10, ma50, ma20, vol]):
        return "HOLD", 0

    # --- Trend ---
    trend = 1 if ma10 > ma50 else -1

    # --- Mean Reversion ---
    z = (current_price - ma20) / vol if vol != 0 else 0

    if z < -2:
        mr = 1
    elif z > 2:
        mr = -1
    else:
        mr = 0

    # --- Regime Detection ---
    if vol > ma20 * 0.002:  # volatility threshold (tune this)
        regime = "volatile"
    elif abs(ma10 - ma50) / ma50 > 0.001:
        regime = "trending"
    else:
        regime = "sideways"

    # --- Signal Fusion ---
    if regime == "trending":
        signal = 0.7 * trend + 0.3 * mr
    elif regime == "sideways":
        signal = 0.3 * trend + 0.7 * mr
    else:
        signal = 0  # volatile ? no trading

    # --- Expected Return Filter ---
    expected_return = abs(signal) * vol

    if expected_return < 0.003:
        signal = 0

    if abs(signal) < 0.6:
        signal = 0

    # --- Drawdown Logic ---
    equity_peak = max(equity_peak, equity)
    drawdown = (equity_peak - equity) / equity_peak if equity_peak > 0 else 0

    position_size = k / vol if vol > 0 else 0

    if drawdown > 0.12:
        position_size = 0
    elif drawdown > 0.08:
        position_size *= 0.5

    # --- Final Decision ---
    if signal > 0 and position == 0:
        position = 1
        entry_price = current_price
        return "BUY", position_size

    elif signal < 0 and position == 1:
        position = 0

        # update equity (simulation)
        pnl = current_price - entry_price
        equity += pnl

        return "SELL", position_size

    return "HOLD", 0
'''

# Test new strategy
import statistics
import csv
state = {}
EXPECTED_RETURN = 0.004
ABSSIGNAL = 0.6
def load_prices_from_csv(filename="price_log.csv"):
    from pair_selector import pair_history

    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                pair = row[1]
                price = float(row[2])

                # ✅ update pair_selector memory
                if pair not in pair_history:
                    pair_history[pair] = []
                pair_history[pair].append(price)
                pair_history[pair] = pair_history[pair][-50:]

                # ✅ update strategy memory
                init_pair(pair)
                state[pair]["prices"].append(price)
                state[pair]["prices"] = state[pair]["prices"][-50:]

        print("CSV data loaded into strategy")

    except FileNotFoundError:
        print("No price_log.csv found")

def init_pair(pair):
    if pair not in state:
        state[pair] = {
            "pnl":0,
            "prices": [],
            "position": 0,
            "quantity": 0,
            "entry_price": None
        }

def yow_strategy(pair, current_price):
    init_pair(pair)

    s = state[pair]
    s["prices"].append(current_price)

    if len(s["prices"]) < 50:
        return "HOLD", 0

    prices = s["prices"]

    ma10 = sum(prices[-10:]) / 10
    ma50 = sum(prices[-50:]) / 50
    ma20 = sum(prices[-20:]) / 20
    vol = statistics.stdev(prices[-20:])

    trend = 1 if ma10 > ma50 else -1

    z = (current_price - ma20) / vol if vol != 0 else 0

    if z < -2:
        mr = 1
    elif z > 2:
        mr = -1
    else:
        mr = 0

    # Regime
    if vol > ma20 * 0.002:
        regime = "volatile"
    elif abs(ma10 - ma50) / ma50 > 0.001:
        regime = "trending"
    else:
        regime = "sideways"

    # Combine
    if regime == "trending":
        signal = 0.7 * trend + 0.3 * mr
    elif regime == "sideways":
        signal = 0.3 * trend + 0.7 * mr
    else:
        signal = 0

    expected_return = abs(signal) * vol

    if expected_return < EXPECTED_RETURN:
        signal = 0

    if abs(signal) < ABSSIGNAL:
        signal = 0

    # Decision
    if signal > 0 and s["position"] == 0:
        s["position"] = 1
        s["entry_price"] = current_price
        return "BUY", None

    elif signal < 0 and s["position"] == 1:
        s["position"] = 0
        pnl = current_price - s["entry_price"]
        s["pnl"] += pnl
        print(f"{pair} PnL: {s['pnl']:.4f}")
        qty = s["quantity"]
        s["position"] = 0
        s["quantity"] = 0

        return "SELL", qty

    return ("HOLD", 0)