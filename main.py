# main.py
import time
from api import *
from strategy import *
from config import PAIR
from logger import init_log, log_trade

def run_bot():
    last_action = None  # prevent repeated trades

    while True:
        data = get_ticker(PAIR)

        if data and data["Success"]:
            price = data["Data"][PAIR]["LastPrice"]
            print(f"Price: {price}")

            action, size = yow_strategy(price)
            print(f"Action: {action}, Size: {size:.6f}")

            #  EXECUTE TRADE
            if action == "BUY" and last_action != "BUY":
                print("BUY signal")

                if LIVE_TRADING:
                    result = place_order(PAIR, "BUY", TRADE_AMOUNT)
                else:
                    # 🧪 SIMULATION
                    result = {
                        "Success": True,
                        "OrderDetail": {
                            "Price": price,
                            "Quantity": TRADE_AMOUNT,
                            "OrderID": "SIMULATED",
                            "Status": "FILLED"
                        }
                    }

                if result and result["Success"]:
                    order = result["OrderDetail"]
                    log_trade(
                        "BUY",
                        PAIR,
                        order["Price"],
                        order["Quantity"],
                        order["OrderID"],
                        order["Status"]
                    )

                last_action = "BUY"

            elif action == "SELL" and last_action != "SELL":
                print("SELL signal")

                if LIVE_TRADING:
                    result = place_order(PAIR, "SELL", TRADE_AMOUNT)
                else:
                    result = {
                        "Success": True,
                        "OrderDetail": {
                            "Price": price,
                            "Quantity": TRADE_AMOUNT,
                            "OrderID": "SIMULATED",
                            "Status": "FILLED"
                        }
                    }

                if result and result["Success"]:
                    order = result["OrderDetail"]
                    log_trade(
                        "SELL",
                        PAIR,
                        order["Price"],
                        order["Quantity"],
                        order["OrderID"],
                        order["Status"]
                    )

                last_action = "SELL"

        else:
            print("Failed to get data")

        time.sleep(10)

def test_ticker():
    data = get_ticker(PAIR)
    
    if data and data["Success"]:
        price = data["Data"][PAIR]["LastPrice"]
        print("Ticker working ")
        print("Price:", price)
    else:
        print("Ticker failed ")
        print(data)

def test_balance():
    data = get_balance()
    print(data)

def test_trade():
    result = place_order(
        pair_or_coin="BTC/USD",
        side="BUY",
        quantity=0.001   # small amount
    )

    print(result)

if __name__ == "__main__":
    init_log()
    run_bot()
    