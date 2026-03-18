import requests
import time
import hmac
import hashlib
from config import API_KEY, SECRET_KEY

BASE_URL = "https://mock-api.roostoo.com"

def _get_timestamp():
    return str(int(time.time() * 1000))

def _get_signed_headers(payload):
    payload['timestamp'] = _get_timestamp()
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

def get_ticker(pair):
    url = f"{BASE_URL}/v3/ticker"
    params = {'timestamp': _get_timestamp(), 'pair': pair}

    try:
        res = requests.get(url, params=params)
        return res.json()
    except Exception as e:
        print("Error:", e)
        return None