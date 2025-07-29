# 📈 NSE Breakout Stock Screener (Streamlit)

This is a Streamlit web app that screens all NSE stocks and identifies breakout opportunities based on:

- 📌 Near breakout (20D or 52-week high)
- 🔊 Volume surge
- 📈 Upward momentum (RSI + MACD)
- 📊 Ranks by profit potential

## 🔧 Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🌐 Deploy on Streamlit Cloud

1. Upload this repo to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New App", link your GitHub
4. Choose `streamlit_app.py` and click Deploy
