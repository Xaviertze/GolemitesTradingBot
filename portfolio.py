import statistics
from api import get_balance
from strategy import state, init_pair
import time

_last_balance = 0
_last_update = 0
returns_history = []
last_equity = None
peak_equity = 0

def get_total_capital_cached():
    global _last_balance, _last_update

    # refresh every 60 sec
    if time.time() - _last_update > 60:
        _last_balance = get_total_capital()
        _last_update = time.time()

    return _last_balance

def get_total_capital():
    data = get_balance()

    # ✅ check API success
    if not data or not data.get("Success"):
        print("Balance API failed:", data)
        return 0

    wallet = data.get("SpotWallet", {})

    usd = wallet.get("USD", {})

    free = usd.get("Free", 0)
    locked = usd.get("Lock", 0)

    return free 



def calculate_volatility(prices):
    if len(prices) < 20:
        return 1  # avoid divide by zero

    return statistics.stdev(prices[-20:])


def get_position_size(pair, state):
    if pair not in state or len(state[pair]["prices"]) <20:
        return 1
    prices = state[pair]["prices"]
    vol = calculate_volatility(prices)

    if vol == 0:
        vol = 1

    # inverse volatility weighting
    raw_size = 1 / vol

    return raw_size


def normalize_sizes(pairs, state):
    sizes = {}
    total = 0

    # compute raw weights
    for pair in pairs:
        size = get_position_size(pair, state)
        sizes[pair] = size
        total += size
    if total  ==0:
        return {pair:1/len(pairs) for pair in pairs}
    # normalize to capital %
    for pair in sizes:
        sizes[pair] = sizes[pair] / total

    return sizes

def adjust_quantity(pair, quantity, pair_rules):
    precision = pair_rules[pair]["AmountPrecision"]

    factor = 10 ** precision

    # 🔥 floor but NEVER drop to zero if valid
    adjusted = int(quantity * factor) / factor

    # 🚨 if becomes zero → force minimum step
    if adjusted == 0:
        adjusted = 1 / factor

    return adjusted

def allocate_trade_size(pair, weights, price, pair_rules):
    capital = get_total_capital_cached()
    if capital == 0 or pair not in weights:
        return 0

    allocation = capital * weights[pair]

    # 🔥 ensure minimum allocation FIRST
    if allocation < 1:
        allocation = 1

    quantity = allocation / price

    quantity = adjust_quantity(pair, quantity, pair_rules)

    # 🔥 FINAL SAFETY CHECK
    if quantity * price < 1:
        quantity = (1 / price)
        quantity = adjust_quantity(pair, quantity, pair_rules)
    return quantity

    


def update_returns(current_equity):
    global last_equity

    # ❗ skip invalid values
    if current_equity == 0:
        return

    if last_equity is None or last_equity == 0:
        last_equity = current_equity
        return

    ret = (current_equity - last_equity) / last_equity
    returns_history.append(ret)

    if len(returns_history) > 100:
        returns_history.pop(0)

    last_equity = current_equity



def get_drawdown(current_equity):
    global peak_equity

    if current_equity > peak_equity:
        peak_equity = current_equity

    drawdown = (peak_equity - current_equity) / peak_equity if peak_equity > 0 else 0

    return drawdown



def load_positions_from_wallet():
    data = get_balance()

    if not data or not data.get("Success"):
        print("Failed to load wallet")
        return

    wallet = data.get("SpotWallet", {})

    for asset, info in wallet.items():
        if asset == "USD":
            continue

        quantity = info.get("Free", 0)

        if quantity > 0:
            pair = f"{asset}/USD"

            init_pair(pair)

            state[pair]["position"] = 1
            state[pair]["quantity"] = quantity

            print(f"Loaded position: {pair} → {quantity}")