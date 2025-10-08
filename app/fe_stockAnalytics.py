import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def compute_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal_Line']
    return df

def app():
    st.title("📊 MACD Visualization for Stock Analysis")
    st.markdown("""In this study, we develop a **stock analysis model** that utilizes the **Support and Resistance approach** to identify
    potential entry and exit zones while confirming price movement strength through **volume analysis**. The methodology,
    code implementation, and data processing details — including **historical price retrieval, pivot-based level computation (S1–R2),
    Volume confirmation**, and **fair value estimation** for buy/sell decisions — are explained in my publication
    *“Stock Analysis Using Support and Resistance”* (available on Google Scholar).""")
    
    tickers = st.multiselect("Select Stock Tickers:", ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK", "TLKM.JK", "ANTM.JK"],
                             default=["BBRI.JK", "BBCA.JK"])

    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-10-07"))        

    if st.button("🔍 Show MACD Chart"):
        st.info("Fetching data and calculating MACD...")
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
        results = pd.DataFrame({t: stockAnalytics(data[t]) for t in tickers}).T
        st.success("✅ Analysis Complete")
        st.subheader("📋 Support, Resistance & Fair Value Summary")
        st.dataframe(results[['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']])

        for t in tickers:
            st.subheader(f"📈 {t} — MACD Indicator")
            df = data[t].copy()
            df = compute_macd(df)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df.index, df['MACD'], label='MACD', color='blue', linewidth=1.5)
            ax.plot(df.index, df['Signal_Line'], label='Signal Line', color='red', linewidth=1.2)
            ax.bar(df.index, df['MACD_Hist'],
                   color=['green' if v >= 0 else 'red' for v in df['MACD_Hist']],
                   alpha=0.4, label='Histogram')
            ax.axhline(0, color='gray', linewidth=0.8)
            ax.legend(loc="upper left", fontsize=8)
            ax.set_title(f"{t} — MACD Momentum Indicator", fontsize=12)
            ax.grid(alpha=0.3)
            st.pyplot(fig)

            latest_macd = df['MACD'].iloc[-1]
            latest_signal = df['Signal_Line'].iloc[-1]
            if latest_macd > latest_signal:
                st.markdown("💹 **Buy Signal:** MACD crosses above the signal line (bullish momentum).")
            elif latest_macd < latest_signal:
                st.markdown("🔻 **Sell Signal:** MACD crosses below the signal line (bearish momentum).")
            else:
                st.markdown("⚖️ **Neutral:** No clear crossover detected.")

# Jalankan aplikasi
if __name__ == "__main__":
    app()
