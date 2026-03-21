import csv
import os
from datetime import datetime

PRICE_FILE = "price_log.csv"
TRADE_FILE = "trade_log.csv"


# ✅ INIT FILES
def init_logs():
    # Price log
    if not os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "pair", "price"])

    # Trade log
    if not os.path.exists(TRADE_FILE):
        with open(TRADE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "action", "pair", "price", "quantity", "mode", "order_id", "status"])


# ✅ LOG PRICE
def log_price(pair, price):
    with open(PRICE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), pair, price])


# ✅ LOG TRADE
def log_trade(pair, action, price, quantity, mode="SIM", order_id="SIMULATED", status="FILLED"):
    from datetime import datetime
    import csv

    with open("trade_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            action,
            pair,
            price,
            quantity,
            mode,
            order_id,
            status
        ])