
import streamlit as st
from model_utils import run_model

st.title("🧠 Krypto Signal-Bot")
st.markdown("📈 Nur Long · 📰 News-Sentiment · 🤖 ML-Modell")

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
selected_coin = coin_map[coin_name]

try:
    df_signals = run_model(selected_coin)
    st.write(f"### 🚦 Aktuelle Signale für {coin_name}")
    st.dataframe(df_signals.tail(30)[['price', 'SMA_10', 'SMA_30', 'RSI', 'sentiment', 'Signal', 'Recommendation']])
except Exception as e:
    st.error(f"Fehler beim Laden der Signale: {e}")
