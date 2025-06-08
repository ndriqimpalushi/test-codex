# Test Codex

This repository contains simple examples.

## Sniper Bot

The `sniper_bot.py` script monitors new Uniswap V2 pairs using The Graph API. Any pair with a daily volume above the threshold is logged to the console.

### Requirements

- Python 3.8+
- `requests` library

Install dependencies:

```bash
pip install requests
```

### Usage

Run the bot:

```bash
python sniper_bot.py
```

It will poll for new pairs every 30 seconds and print those with high volume.
