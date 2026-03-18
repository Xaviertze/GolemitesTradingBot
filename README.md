Roostoo AI Trading Bot
1. Overview

This project is an automated cryptocurrency trading bot developed for the Roostoo AI Web3 Trading Bot Competition.

The bot interacts with the Roostoo exchange via REST APIs and executes trades autonomously based on a predefined strategy. It is designed to maximize portfolio returns while maintaining controlled risk exposure.

2. Strategy Explanation
Strategy Type

Currently implemented:

Rule-based strategy (baseline)

Designed to be extendable into:

Momentum strategies

Mean reversion strategies

Machine learning / reinforcement learning models

Entry Conditions

BUY when price is below a defined threshold (undervalued signal)

SELL when price is above a defined threshold (overvalued signal)

(Note: This is a simple baseline strategy for testing API integration and execution logic. It will be refined further.)

Exit Conditions

Positions are closed based on inverse signals (BUY → SELL, SELL → BUY)

Risk Management

Fixed position sizing per trade

Avoid excessive trading (API limit: 30 calls/min)

Commission-aware execution:

0.1% (market orders)

0.05% (limit orders)

Designed to be extended with:

Stop-loss

Take-profit

Drawdown control

3. Architecture

The project is modular for clarity and scalability:

project/
├── main.py        # Entry point (runs the bot loop)
├── api.py         # Handles all API communication
├── strategy.py    # Trading logic
├── config.py      # Configuration and environment variables
├── .env           # API keys (not committed)
├── .gitignore     # Prevents sensitive files from being tracked
Module Responsibilities

api.py

Handles authentication (HMAC SHA256)

Sends GET/POST requests to Roostoo endpoints

Manages headers and payload signing

strategy.py

Contains trading decision logic

Outputs BUY / SELL / HOLD signals

main.py

Runs continuous trading loop

Fetches market data

Calls strategy

Executes trades

config.py

Loads environment variables

Stores trading parameters

4. API Integration

The bot uses the following Roostoo endpoints:

/v3/ticker → Market price data

/v3/place_order → Execute trades

/v3/balance → Portfolio tracking

/v3/query_order → Order history

Authentication:

HMAC SHA256 signature

Timestamp-based validation

Headers:

RST-API-KEY

MSG-SIGNATURE

5. Setup Instructions
Step 1: Clone the repository
git clone <your-repo-url>
cd <project-folder>
Step 2: Install dependencies
pip install -r requirements.txt
Step 3: Set API keys

Create a .env file in the root directory:

API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

⚠️ Do NOT share or upload this file.

Step 4: Run the bot
python main.py
6. Deployment (AWS EC2)

The bot is designed to run on AWS EC2:

Region: ap-southeast-2 (Sydney)

Instance: t3.medium

Connection: Session Manager

To keep the bot running:

tmux
python main.py

Detach session:

Ctrl + B, then D
7. Logging & Monitoring

The bot is designed to log:

Timestamp

Trading pair

Action (BUY / SELL)

Price

Quantity

API response

Future improvements:

Performance tracking (PnL)

Risk metrics (Sharpe, Sortino, Calmar)

8. Constraints & Considerations

API rate limit: 30 requests per minute

No high-frequency trading allowed

Only spot trading (no leverage or shorting)

Commission costs impact profitability

Strategy must be fully autonomous (no manual intervention)

9. Future Improvements

Advanced trading strategies:

Moving average crossover

RSI / MACD indicators

Machine learning models (e.g., PPO agents)

Dynamic position sizing

Risk-adjusted optimization

Backtesting using Binance historical data

10. Notes

This bot is built for educational and competitive purposes.

The current implementation focuses on:

Correct API integration

Stable execution

Expandable architecture

11. Disclaimer

This is a mock trading environment. No real funds are used.

Trading strategies may carry risk in real-world scenarios and should be tested thoroughly before live deployment.