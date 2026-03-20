import statistics
from api import get_balance
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

    wallet = data.get("Wallet", {})

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


def allocate_trade_size(pair, weights, price):
    capital = get_total_capital_cached()

    if capital == 0:
        return 0

    drawdown = get_drawdown(capital)

    # 🔥 risk control
    if drawdown > 0.12:
        return 0  # STOP trading

    allocation = capital * weights[pair]

    # reduce size if losing
    if drawdown > 0.08:
        allocation *= 0.5

    quantity = allocation / price

    return min(round(quantity, 6), 0.01)


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