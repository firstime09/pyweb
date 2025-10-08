import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from app import myfunction as mf

stockAnalytics = mf.allFunction.calc_levels_with_fair_value

def compute_macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal_Line']
    return df

def app():
    st.title("📊 Advanced Stock Analysis: Support, Resistance & MACD Visualization")

    # Pilihan saham
    tickers = st.multiselect(
        "Select Stock Tickers:",
        ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"],
        default=["BBRI.JK"])

    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-08-08"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-10-07"))

    if st.button("🔍 Run Analysis"):
        st.info("Fetching data and performing analysis...")
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
        results = pd.DataFrame({t: stockAnalytics(data[t]) for t in tickers}).T
        st.success("✅ Analysis Complete")

        st.subheader("📋 Support, Resistance & Fair Value Summary")
        st.dataframe(results[['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']])

        for t in tickers:
            df = data[t].copy()
            df = compute_macd(df)  # Tambahkan MACD

            st.markdown(f"### 📈 {t} — Price, Support, Resistance, and MACD")

            S1 = results.loc[t, 'S1']
            Pivot = results.loc[t, 'Pivot']
            R1 = results.loc[t, 'R1']
            Fair_Buy = results.loc[t, 'Fair_Buy']
            Fair_Sell = results.loc[t, 'Fair_Sell']

            # --- Plot harga dan level support/resistance
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True,
                                           gridspec_kw={'height_ratios': [3, 1]})
            
            # Grafik harga
            ax1.plot(df.index, df['Close'], color='black', linewidth=2, label='Close Price')
            ax1.axhline(S1, color='green', linestyle='--', linewidth=1.2, label=f'Support (S1): {S1:.2f}')
            ax1.axhline(Pivot, color='blue', linestyle=':', linewidth=1.2, label=f'Pivot: {Pivot:.2f}')
            ax1.axhline(R1, color='red', linestyle='--', linewidth=1.2, label=f'Resistance (R1): {R1:.2f}')
            ax1.axhline(Fair_Buy, color='lime', linestyle='-.', linewidth=1.2, label=f'Fair Buy: {Fair_Buy:.2f}')
            ax1.axhline(Fair_Sell, color='orange', linestyle='-.', linewidth=1.2, label=f'Fair Sell: {Fair_Sell:.2f}')
            ax1.legend(loc="upper left", fontsize=8)
            ax1.set_title(f"{t} Price with Support & Resistance", fontsize=13)
            ax1.grid(alpha=0.3)

            # --- Plot MACD
            ax2.plot(df.index, df['MACD'], label='MACD', color='blue', linewidth=1.5)
            ax2.plot(df.index, df['Signal_Line'], label='Signal Line', color='red', linewidth=1.2)
            ax2.bar(df.index, df['MACD_Hist'], color=['green' if v >= 0 else 'red' for v in df['MACD_Hist']],
                    alpha=0.4, label='Histogram')
            ax2.legend(loc="upper left", fontsize=8)
            ax2.set_title("MACD Indicator", fontsize=11)
            ax2.axhline(0, color='gray', linewidth=0.8)
            ax2.grid(alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig)

            # --- Interpretasi sinyal MACD
            latest_macd = df['MACD'].iloc[-1]
            latest_signal = df['Signal_Line'].iloc[-1]
            if latest_macd > latest_signal:
                signal_text = "💹**Buy Signal:** MACD crosses above the signal line (bullish momentum)."
            elif latest_macd < latest_signal:
                signal_text = "🔻**Sell Signal:** MACD crosses below the signal line (bearish momentum)."
            else:
                signal_text = "⚖️**Neutral:** No clear momentum crossover yet."

            st.markdown(f"""
            **Interpretation for {t}:**
            - Current Close Price: `{df['Close'][-1]:,.2f}`
            - Support Zone: `{S1:,.2f} - {Pivot:,.2f}` → *Potential Buy Area*
            - Resistance Zone: `{Pivot:,.2f} - {R1:,.2f}` → *Potential Profit Area*
            - Fair Buy: `{Fair_Buy:,.2f}`, Fair Sell: `{Fair_Sell:,.2f}`
            - Trend Signal: **{results.loc[t, 'Trend_Signal']}**
            - MACD Status: {signal_text}
            """)

# Run locally
if __name__ == "__main__":
    app()
