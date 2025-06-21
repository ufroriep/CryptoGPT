
import streamlit as st
from model_utils import run_model

st.title("Krypto Signal-Bot")
st.markdown("📈 **Long only** · 🔍 Machine Learning · 📰 News-Sentiment")

coin_map = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
    "Avalanche": "avalanche-2",
    "TRON": "tron",
    "Polkadot": "polkadot"
}

coin_name = st.selectbox("🔎 Wähle einen Coin", list(coin_map.keys()))
df_signals = run_model(coin_map[coin_name])

st.write(f"### 🚦 Aktuelle Signale für {coin_name}")
st.dataframe(df_signals.tail(30)[['price', 'SMA_10', 'SMA_30', 'RSI', 'sentiment', 'Signal', 'Recommendation']])
