
import pandas as pd
import requests

API_KEY = "DEIN_API_KEY_HIER"

def fetch_historical_data(coin_id='BTC', days=180):
    symbol_map = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        'binancecoin': 'BNB',
        'ripple': 'XRP',
        'cardano': 'ADA',
        'dogecoin': 'DOGE',
        'avalanche-2': 'AVAX',
        'tron': 'TRX',
        'polkadot': 'DOT'
    }

    if coin_id not in symbol_map:
        raise ValueError(f"🛑 Coin-ID '{coin_id}' wird nicht unterstützt.")

    symbol = symbol_map[coin_id]
    market = 'USD'
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol,
        "market": market,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ValueError(f"❌ AlphaVantage API-Fehler: {response.status_code} – {response.text}")

    data = response.json()
    if "Time Series (Digital Currency Daily)" not in data:
        raise ValueError(f"📉 AlphaVantage lieferte keine gültigen Daten für {coin_id} ({symbol}).")

    ts = data["Time Series (Digital Currency Daily)"]
    df = pd.DataFrame.from_dict(ts, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Robuster Preiszugriff mit Fallbacks
    for key in ['4a. close (USD)', '4b. close (USD)', '4. close']:
        if key in df.columns:
            df['price'] = df[key].astype(float)
            break
    else:
        raise ValueError("❌ Konnte kein gültiges Preisfeld finden (4a/4b/4). Struktur geändert?")

    df = df[['price']]
    df = df.tail(days)

    return df
