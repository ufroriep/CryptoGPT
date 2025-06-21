
import pandas as pd
import requests
from datetime import datetime

def fetch_historical_data(coin_id='bitcoin', days=180):
    # Mapping CoinGecko-ID zu Binance Symbol
    symbol_map = {
        'bitcoin': 'BTCUSDT',
        'ethereum': 'ETHUSDT',
        'solana': 'SOLUSDT',
        'binancecoin': 'BNBUSDT',
        'ripple': 'XRPUSDT',
        'cardano': 'ADAUSDT',
        'dogecoin': 'DOGEUSDT',
        'avalanche-2': 'AVAXUSDT',
        'tron': 'TRXUSDT',
        'polkadot': 'DOTUSDT'
    }

    if coin_id not in symbol_map:
        raise ValueError(f"Coin {coin_id} nicht unterstützt für Binance.")

    symbol = symbol_map[coin_id]
    limit = days
    interval = '1d'

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])

    df['price'] = df['close'].astype(float)
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    df = df[['price']]

    return df
