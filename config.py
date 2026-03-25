import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
SECRET_KEY =os.getenv("SECRET_KEY")


DEBUG = False
PAIR = "BTC/USD"
LIVE_TRADING = True
TRADE_AMOUNT = 0.001

BANNED_COINS = ["TAO"]
BANNED_PAIRS = ["TAO/USD"]