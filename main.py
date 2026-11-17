import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

import makefun_bars


SYMBOL = "CBBTC"
TREND_BARS = 120
PEAK_BARS = 240
REBOUND_BARS = 15
PULLBACK_BPS = 80
TAKE_PROFIT_BPS = 80
STOP_LOSS_BPS = 200
POSITION_BPS = 9_500
COOLDOWN_BARS = 15
MAX_SLIPPAGE_BPS = 1_000
HISTORY_LIMIT = PEAK_BARS

closes = []
cooldown_until = -1


def on_batch(state, batch):
    global cooldown_until

    bar = next((item for item in batch["bars"] if item["symbol"] == SYMBOL), None)
    if bar is None:
        return []

    close = int(bar["c"])
    closes.append(close)
    if len(closes) > HISTORY_LIMIT:
        del closes[0]

    if any(fill["side"] == "sell" and fill["status"] == "filled" for fill in batch["fills"]):
        cooldown_until = state.seq + COOLDOWN_BARS

    if state.warming_up or state.seq >= 1_439:
        return []

    holding = state.positions.get(SYMBOL)
    if holding is not None:
        marked_value = state.value(SYMBOL, holding.qty)
        if (
            marked_value * 10_000 >= holding.cost * (10_000 + TAKE_PROFIT_BPS)
            or marked_value * 10_000 <= holding.cost * (10_000 - STOP_LOSS_BPS)
        ):
            return [{
                "side": "sell",
                "symbol": SYMBOL,
                "qty": holding.qty,
                "max_slippage_bps": MAX_SLIPPAGE_BPS,
            }]
        return []

    if state.seq < cooldown_until or len(closes) < TREND_BARS:
        return []

    trend = sum(closes[-TREND_BARS:]) // TREND_BARS
    peak = max(closes[-PEAK_BARS:])
    recovered = close > closes[-REBOUND_BARS - 1]
    pulled_back = close * 10_000 <= peak * (10_000 - PULLBACK_BPS)
    if close <= trend or not pulled_back or not recovered:
        return []

    caps = state.hello["caps"]
    max_weight = caps["max_weight_bps"] * state.equity // 10_000
    notional = min(
        state.cash * POSITION_BPS // 10_000,
        max_weight,
    )
    if notional < int(state.hello["fees"]["min_notional_quote_units"]):
        return []

    return [{
        "side": "buy",
        "symbol": SYMBOL,
        "notional_quote_units": notional,
        "max_slippage_bps": MAX_SLIPPAGE_BPS,
    }]


makefun_bars.run(on_batch)
