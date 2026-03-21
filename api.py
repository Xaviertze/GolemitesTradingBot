import requests
import time
import hmac
import hashlib
from config import *

BASE_URL = "https://mock-api.roostoo.com"

def _get_timestamp():
    return str(int(time.time() * 1000))

def _get_signed_headers(payload: dict):
    payload['timestamp'] = _get_timestamp()

    # Sort params
    sorted_keys = sorted(payload.keys())
    total_params = "&".join(f"{k}={payload[k]}" for k in sorted_keys)

    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        total_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        'RST-API-KEY': API_KEY,
        'MSG-SIGNATURE': signature
    }

    return headers, payload

def get_ticker(pair=None):
    url = f"{BASE_URL}/v3/ticker"
    params = {'timestamp': _get_timestamp()}

    if pair:
        params['pair'] = pair

    try:
        res = requests.get(url, params=params)
        return res.json()
    except Exception as e:
        print("Error:", e)
        return None

def get_balance():
    url = "https://mock-api.roostoo.com/v3/balance"

    payload = {}

    headers, payload = _get_signed_headers(payload)

    try:
        response = requests.get(url, headers=headers, params=payload)
        if DEBUG :
            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)  

        return response.json()

    except Exception as e:
        print("Error:", e)
        return None

def place_order(pair_or_coin, side, quantity, price=None, order_type=None):
    url = "https://mock-api.roostoo.com/v3/place_order"

    pair = pair_or_coin if "/" in pair_or_coin else f"{pair_or_coin}/USD"

    if order_type is None:
        order_type = "LIMIT" if price is not None else "MARKET"

    if order_type == "LIMIT" and price is None:
        print("Error: LIMIT orders require price")
        return None

    payload = {
        "pair": pair,
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": str(quantity)
    }

    if order_type == "LIMIT":
        payload["price"] = str(price)

    headers, payload = _get_signed_headers(payload)
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    # MUST MATCH SIGNATURE ORDER
    sorted_keys = sorted(payload.keys())
    total_params = "&".join(f"{k}={payload[k]}" for k in sorted_keys)

    try:
        response = requests.post(url, headers=headers, data=total_params)

        if DEBUG:
            print("STATUS:", response.status_code)
            print("RAW:", response.text)

        return response.json()

    except Exception as e:
        print("Error placing order:", e)
        return None
    
def get_all_pairs():
    url = f"{BASE_URL}/v3/exchangeInfo"

    try:
        res = requests.get(url)
        data = res.json()
        return list(data["TradePairs"].keys())
    except Exception as e:
        print("Error getting pairs:", e)
        return []

def get_exchange_info():
    url = f"{BASE_URL}/v3/exchangeInfo"
    return requests.get(url).json()