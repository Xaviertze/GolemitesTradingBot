import statistics
from config import *

pair_history = {}

def update_pair_history(pair, price):
    if pair not in pair_history:
        pair_history[pair] = []

    pair_history[pair].append(price)

    # keep last 20 points
    pair_history[pair] = pair_history[pair][-50:]


def score_pair(pair):
    prices = pair_history.get(pair, [])

    if len(prices) < 10:
        return 0

    vol = statistics.stdev(prices)
    change = (prices[-1] - prices[0]) / prices[0]

    score = abs(change) * vol
    return score


def select_top_pairs(all_pairs, top_n=3):
    scores = []

    for pair in all_pairs:
        coin = pair.split("/")[0]
        if coin in BANNED_COINS or pair in BANNED_PAIRS:
            continue
        score = score_pair(pair)
        scores.append((pair, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return [p for p, _ in scores[:top_n]]


    

    