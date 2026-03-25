# main.py
'''
import time
from api import *
from strategy import *
from config import PAIR
from logger import *

def run_bot():
    last_action = None  # prevent repeated trades

    while True:
        data = get_ticker(PAIR)

        if data and data["Success"]:
            price = data["Data"][PAIR]["LastPrice"]
            log_price(PAIR,price)
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
    load_prices_from_csv()
    run_bot()
    
    test_balance()
'''

# Test new code
import time
from api import *
from strategy import *
import pair_selector
from config import *
from logger import *
import portfolio

all_pairs = []
selected_pairs = []
last_selected_pairs = []

def run_bot():
    global selected_pairs
    global last_selected_pairs

    counter = 0
    data_counter = 0

    while True:
        capital = portfolio.get_total_capital_cached()
        portfolio.update_returns(capital)
        counter += 1

        if data_counter % 4 == 0:
            print("Collecting market data...")

            data = get_ticker(None)

            if data and data["Success"]:
                for pair, info in data["Data"].items():
                    price = info["LastPrice"]

                    pair_selector.update_pair_history(pair, price)
                    log_price(pair, price)

        data_counter += 1

        # 🔄 Update pair selection every ~1 minute
        if counter % 4 == 0:
            new_pairs = pair_selector.select_top_pairs(all_pairs,top_n=3)

            if set(new_pairs) != set(selected_pairs):
                last_selected_pairs = selected_pairs
                selected_pairs = new_pairs
                print("Updated pairs :", selected_pairs)
        if not selected_pairs:
            continue
        else:
            weights = portfolio.normalize_sizes(selected_pairs,state)

        for pair in selected_pairs:
            data = get_ticker(pair)

            if data and data["Success"]:
                price = data["Data"][pair]["LastPrice"]

                pair_selector.update_pair_history(pair, price)

                action, strat_size = yow_strategy(pair, price)
                    
                print(f"{pair} | Price: {price} | Action: {action}")
                
                if action == "BUY":
                    size = portfolio.allocate_trade_size(pair, weights, price, pair_rules)
                    if size <= 0 or size * price < 1:
                            print(f"Skipping {action} {pair} — invalid size")
                            continue
                    if LIVE_TRADING:
                        result = place_order(pair, "BUY", size)
                        if result and result.get("Success"):
                            order = result["OrderDetail"]

                            log_trade(
                                pair,
                                "BUY",
                                order["Price"],
                                order["Quantity"],
                                mode="LIVE",
                                order_id=order["OrderID"],
                                status=order["Status"]
                            )

                            # ✅ STORE ACTUAL FILLED QUANTITY
                            state[pair]["quantity"] = order["Quantity"]
                            state[pair]["entry_price"] = order["Price"]
                        else:
                            print("BUY failed:", result)

                    else:
                        print(f"SIM BUY {pair}")

                        log_trade(pair, "BUY", price, size)

                elif action == "SELL":
                    size = strat_size
                    if size <= 0 or size * price < 1:
                            print(f"Skipping {action} {pair} — invalid size")
                            continue
                    
                    if LIVE_TRADING:
                        result = place_order(pair, "SELL", size)

                        if result and result.get("Success"):
                            order = result["OrderDetail"]

                            log_trade(
                                pair,
                                "SELL",
                                order["Price"],
                                order["Quantity"],
                                mode="LIVE",
                                order_id=order["OrderID"],
                                status=order["Status"]
                            )
                        else:
                            print("SELL failed:", result)

                    else:
                        print(f"SIM SELL {pair}")

                        log_trade(pair, "SELL", price, size)


        time.sleep(15)


if __name__ == "__main__":
    init_logs()
    portfolio.liquidate_banned_assets()
    exchange_info = get_exchange_info()
    pair_rules = exchange_info["TradePairs"]
    load_prices_from_csv()
    portfolio.load_positions_from_wallet()
    all_pairs = get_all_pairs()
    selected_pairs = all_pairs[:3]  # initial fallback
    run_bot()
    