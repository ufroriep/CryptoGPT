import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from data_fetch import fetch_historical_data
from sentiment_utils import fetch_news_sentiment


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def add_indicators(df, sentiment_df):
    df['SMA_10'] = df['price'].rolling(window=10).mean()
    df['SMA_30'] = df['price'].rolling(window=30).mean()
    df['RSI'] = compute_rsi(df['price'])
    df['Return_5d'] = df['price'].pct_change(periods=5)
    df['Future_5d'] = df['price'].pct_change(periods=5).shift(-5)
    df['Label'] = (df['Future_5d'] > 0.01).astype(int)

    # Sentiment-Spalte hinzufügen
    sentiment_df = sentiment_df.rename(columns={'score': 'sentiment'})
    df = df.merge(sentiment_df, left_index=True, right_index=True, how='left')
    df['sentiment'].fillna(method='ffill', inplace=True)
    df['sentiment'].fillna(0.0, inplace=True)

    return df.dropna()


def train_and_predict(df):
    features = ['SMA_10', 'SMA_30', 'RSI', 'Return_5d', 'sentiment']
    X = df[features].dropna()
    y = df.loc[X.index, 'Label']

    if X.empty or y.empty:
        raise ValueError("❌ Keine gültigen Trainingsdaten gefunden. Prüfe Indikatoren oder Sentiment.")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    df['Signal'] = model.predict_proba(X)[:, 1]
    df['Recommendation'] = np.where(df['Signal'] > 0.6, 'BUY', 'HOLD')

    return df


def run_model(coin_id):
    df_raw = fetch_historical_data(coin_id, days=180)
    sentiment = fetch_news_sentiment(coin_id)

    if sentiment is None or sentiment.empty:
        # Fallback auf neutrales Sentiment
        df_raw['sentiment'] = 0.0
        df_raw['SMA_10'] = df_raw['price'].rolling(window=10).mean()
        df_raw['SMA_30'] = df_raw['price'].rolling(window=30).mean()
        df_raw['RSI'] = compute_rsi(df_raw['price'])
        df_raw['Return_5d'] = df_raw['price'].pct_change(periods=5)
        df_raw['Future_5d'] = df_raw['price'].pct_change(periods=5).shift(-5)
        df_raw['Label'] = (df_raw['Future_5d'] > 0.01).astype(int)
        df = df_raw.dropna()
        return train_and_predict(df)

    df_indicators = add_indicators(df_raw.copy(), sentiment)
    df_signals = train_and_predict(df_indicators.copy())
    return df_signals
