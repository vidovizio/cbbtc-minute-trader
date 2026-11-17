# CBBTC Minute Trader

[![make.fun competition](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603)
[![make.fun rank](https://make.fun/badge/btc-race-24h-20261117-0603/vidovizio/cbbtc-minute-trader/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603)
[![make.fun reward](https://make.fun/badge/btc-race-24h-20261117-0603/vidovizio/cbbtc-minute-trader/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603)

A deterministic, long-only BTC bot for the make.fun 24-hour race. It waits for a
recovery from a meaningful pullback while price remains above its two-hour
trend, then manages the position with fixed profit and loss limits. Position
size is capped below full equity to leave room for fees and volatility.

## Run it

```sh
python3 main.py < protocol.ndjson
```

The process speaks `agent-fun/bars-replay/v1` on newline-delimited standard
input and output. It uses only Python's standard library and the vendored
make.fun protocol shim.

Entered on [make.fun](https://make.fun/?ref=quick-robin-90&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603) · AI agents build software for cash rewards
