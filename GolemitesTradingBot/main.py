# main.py
import time
from api import get_ticker
from strategy import simple_strategy
from config import PAIR

def run_bot():
    while True:
        data = get_ticker(PAIR)

        if data and data["Success"]:
            price = data["Data"][PAIR]["LastPrice"]
            print(f"Price: {price}")

            action = simple_strategy(price)
            print(f"Action: {action}")

        else:
            print("Failed to get data")

        time.sleep(10)  # avoid rate limit

if __name__ == "__main__":
    run_bot()