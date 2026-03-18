#Roostoo AI Trading Bot
##1. Overview

This project is an automated cryptocurrency trading bot developed for the Roostoo AI Web3 Trading Bot Competition.

The bot interacts with the Roostoo exchange via REST APIs and executes trades autonomously based on a predefined strategy. It is designed to maximize portfolio returns while maintaining controlled risk exposure.

##2. Strategy Explanation
Strategy Type

Currently implemented:

Rule-based strategy (baseline)

Designed to be extendable into:

Momentum strategies

Mean reversion strategies

Machine learning / reinforcement learning models

##3. Project Structure
main.py        # runs the bot
api.py         # handles API calls
strategy.py    # trading logic
config.py      # config & API keys
4. Setup
Install dependencies
pip install requests python-dotenv
Create .env file
API_KEY=your_api_key
SECRET_KEY=your_secret_key
5. Run
python main.py
6. Notes

Fully automated (no manual trading)

Respects API rate limits

Designed for AWS deployment

##7. Disclaimer

This bot is for educational and competition purposes only.