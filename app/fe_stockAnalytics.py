import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from app import myfunction as mf

# Load custom analysis function
stockAnalytics = mf.allFunction.calc_levels_with_fair_value

def app():
    st.title("📊 Stock Analysis Using Support & Resistance")
    st.markdown("""
    In this study, we develop a **stock analysis model** that utilizes the **Support and Resistance approach** 
    to identify potential entry and exit zones while confirming price movement strength through **volume analysis**.  
    The methodology, code implementation, and data processing details — including **historical price retrieval, 
    pivot-based level computation (S1–R2), volume confirmation**, and **fair value estimation** for buy/sell decisions — 
    are explained in my publication *“Stock Analysis Using Support and Resistance”* (available on Google Scholar).
    """)

    # --- User Input Section ---
    tickers = st.multiselect(
        "Select Stock Tickers:",
        ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"],
        default=["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"])

    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-08-08"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-10-07"))

    if st.button("Run Analysis"):
        st.write("Fetching stock data and running analysis... ⏳")
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

        results = pd.DataFrame({t: stockAnalytics(data[t]) for t in tickers}).T
        st.success("✅ Analysis Completed")

        # --- Display Results Table ---
        st.subheader("📈 Support, Resistance, Volume & Fair Value Analysis")
        st.dataframe(results[['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']])

        # --- Plot Section ---
        st.subheader("📉 Price & Volume Visualization")
        for t in tickers:
            df = data[t].copy()
            st.markdown(f"### {t}")
            fig, ax1 = plt.subplots(figsize=(10, 4))
            
            ax1.plot(df.index, df['Close'], label='Close Price', linewidth=1.8)
            ax1.axhline(results.loc[t, 'S1'], color='green', linestyle='--', label='Support (S1)')
            ax1.axhline(results.loc[t, 'R1'], color='red', linestyle='--', label='Resistance (R1)')
            ax1.axhline(results.loc[t, 'Pivot'], color='blue', linestyle=':', label='Pivot')
            ax1.set_ylabel("Price (IDR)")
            ax1.legend(loc="upper left")
            
            ax2 = ax1.twinx()
            ax2.bar(df.index, df['Volume'], color='gray', alpha=0.3, label='Volume')
            ax2.set_ylabel("Volume")

            st.pyplot(fig)

        st.markdown("---")
        st.markdown("💡 *Interpretation:* Stocks trading near the **Support (S1)** may indicate a potential buy zone, "
                    "while those near **Resistance (R1)** could suggest an area for taking profits. "
                    "Volume confirmation strengthens the validity of these signals.")

# Run the app (for local testing)
if __name__ == "__main__":
    app()
