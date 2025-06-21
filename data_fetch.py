
import pandas as pd
import requests
from datetime import datetime, timedelta

def fetch_historical_data(coin_id='btc-bitcoin', days=180):
    id_map = {
        'bitcoin': 'btc-bitcoin',
        'ethereum': 'eth-ethereum',
        'solana': 'sol-solana',
        'binancecoin': 'bnb-binance-coin',
        'ripple': 'xrp-xrp',
        'cardano': 'ada-cardano',
        'dogecoin': 'doge-dogecoin',
        'avalanche-2': 'avax-avalanche',
        'tron': 'trx-tron',
        'polkadot': 'dot-polkadot'
    }

    if coin_id not in id_map:
        raise ValueError(f"🛑 Coin-ID '{coin_id}' nicht in Coinpaprika-ID-Liste.")

    paprika_id = id_map[coin_id]
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    url = f"https://api.coinpaprika.com/v1/coins/{paprika_id}/ohlcv/historical"
    params = {
        'start': start_date.strftime('%Y-%m-%d'),
        'end': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ValueError(f"❌ Coinpaprika API-Fehler: {response.status_code} – {response.text}")

    data = response.json()
    if not data:
        raise ValueError(f"📉 Keine historischen Daten für {coin_id} erhalten.")

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['time_open']).dt.date
    df.set_index('date', inplace=True)
    df['price'] = df['close']
    df = df[['price']]

    return df
