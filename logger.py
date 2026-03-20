import csv
import os
from datetime import datetime

LOG_FILE = "trade_log.csv"

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "action",
                "pair",
                "price",
                "quantity",
                "order_id",
                "status"
            ])

def log_trade(action, pair, price, quantity, order_id, status):
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),
            action,
            pair,
            price,
            quantity,
            order_id,
            status
        ])
        
def log_price(pair, price):
    with open("price_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), pair, price])