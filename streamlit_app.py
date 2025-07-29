import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="NSE Breakout Screener", layout="wide")

@st.cache_data(ttl=3600)
def get_nse_symbols():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    return df['SYMBOL'].dropna().unique().tolist()

def get_stock_data(symbol, period="6mo"):
    try:
        df = yf.download(f"{symbol}.NS", period=period, interval="1d", progress=False)
        if df.empty or len(df) < 30:
            return None
        df.dropna(inplace=True)
        return df
    except:
        return None

def analyze_stock(symbol):
    df = get_stock_data(symbol)
    if df is None:
        return None

    df['volume_avg'] = df['Volume'].rolling(window=20).mean()
    close_series = df['Close'].squeeze()
    df['rsi'] = ta.momentum.RSIIndicator(close=close_series, window=14).rsi()
    macd = ta.trend.MACD(close=close_series)
    df['macd_diff'] = macd.macd_diff()

    close = df['Close'].iloc[-1]
    high_20 = df['High'].rolling(window=20).max().iloc[-1]
    high_52w = df['High'].max()
    volume_today = df['Volume'].iloc[-1]
    avg_volume = df['volume_avg'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    macd_recent = df['macd_diff'].iloc[-1]

    near_breakout = close >= 0.98 * high_20 or close >= 0.95 * high_52w
    volume_spike = volume_today > 1.5 * avg_volume
    bullish_momentum = rsi > 60 and macd_recent > 0

    if near_breakout and volume_spike and bullish_momentum:
        profit_potential = round((high_52w - close) / close * 100, 2)
        return {
            'Symbol': symbol,
            'Close': round(close, 2),
            '20D_High': round(high_20, 2),
            '52W_High': round(high_52w, 2),
            'Volume_Today': volume_today,
            'Avg_Volume': int(avg_volume),
            'RSI': round(rsi, 2),
            'Profit_Potential (%)': profit_potential
        }
    return None

def run_screener():
    symbols = get_nse_symbols()
    breakout_stocks = []

    with st.spinner("🔍 Screening NSE stocks..."):
        for i, symbol in enumerate(symbols):
            result = analyze_stock(symbol)
            if result:
                breakout_stocks.append(result)

    return pd.DataFrame(breakout_stocks)

st.title("📈 NSE Breakout Stock Screener")

if st.button("Run Screener"):
    df = run_screener()
    if not df.empty:
        df.sort_values(by='Profit_Potential (%)', ascending=False, inplace=True)
        st.success(f"✅ Found {len(df)} breakout candidates")
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "nse_breakout_stocks.csv")
    else:
        st.warning("😕 No breakout candidates found.")
else:
    st.info("Click 'Run Screener' to analyze current breakout opportunities on NSE.")
