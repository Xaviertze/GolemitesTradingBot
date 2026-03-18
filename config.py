import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
PAIR = "BTC/USD"
LIVE_TRADING = False
TRADE_AMOUNT = 0.001