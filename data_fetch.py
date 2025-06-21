import pandas as pd
from pycoingecko import CoinGeckoAPI


def fetch_historical_data(coin_id='bitcoin', days=180):
    cg = CoinGeckoAPI()
    data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)

    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    prices.set_index('date', inplace=True)

    # Keine dropna(), damit auch heutiger (nicht vollständiger) Tag bleibt
    prices = prices.resample('1D').mean()

    return prices
