import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from app import myfunction as mf

stockAnalytics = mf.allFunction.calc_levels_with_fair_value

def app():
    st.title("📊 Advanced Stock Analysis: Support & Resistance Visualization")

    tickers = st.multiselect(
        "Select Stock Tickers:",
        ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"],
        default=["BBRI.JK"]
    )

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
            st.markdown(f"### 📈 {t} — Price Movement with Support & Resistance")

            S1 = results.loc[t, 'S1']
            Pivot = results.loc[t, 'Pivot']
            R1 = results.loc[t, 'R1']
            Fair_Buy = results.loc[t, 'Fair_Buy']
            Fair_Sell = results.loc[t, 'Fair_Sell']

            # --- Convert DatetimeIndex to numeric for rectangle plotting
            x_dates = mdates.date2num(df.index)
            x_start = x_dates[0]
            x_end = x_dates[-1]
            width = x_end - x_start

            # --- Plot ---
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df['Open'], color='black', linewidth=2, label='Open Price')

            # Support & Resistance zones
            ax.add_patch(Rectangle((x_start, S1), width=width, height=Pivot - S1,
                                   color='green', alpha=0.1, label='Support Zone'))
            ax.add_patch(Rectangle((x_start, Pivot), width=width, height=R1 - Pivot,
                                   color='red', alpha=0.1, label='Resistance Zone'))

            # Important lines
            ax.axhline(S1, color='green', linestyle='--', linewidth=1.5, label=f'Support (S1): {S1:.2f}')
            ax.axhline(Pivot, color='blue', linestyle=':', linewidth=1.5, label=f'Pivot: {Pivot:.2f}')
            ax.axhline(R1, color='red', linestyle='--', linewidth=1.5, label=f'Resistance (R1): {R1:.2f}')
            ax.axhline(Fair_Buy, color='lime', linestyle='-.', linewidth=1.2, label=f'Fair Buy: {Fair_Buy:.2f}')
            ax.axhline(Fair_Sell, color='orange', linestyle='-.', linewidth=1.2, label=f'Fair Sell: {Fair_Sell:.2f}')

            # --- Formatting ---
            ax.set_title(f"{t} — Support & Resistance Zones", fontsize=14)
            ax.set_ylabel("Price (IDR)")
            ax.legend(loc="upper left", fontsize=8)
            ax.grid(alpha=0.3)
            ax.xaxis_date()
            fig.autofmt_xdate()

            # Volume
            ax2 = ax.twinx()
            ax2.bar(df.index, df['Volume'], color='gray', alpha=0.2, label='Volume')
            ax2.set_ylabel("Volume")
            ax2.set_ylim(0, df['Volume'].max() * 4)

            st.pyplot(fig)

            # --- Interpretation ---
            st.markdown(f"""
            **Interpretation for {t}:**
            - Current Close Price: `{df['Close'][-1]:,.2f}`
            - Support Zone: `{S1:,.2f} - {Pivot:,.2f}` → *Potential Buy Area*
            - Resistance Zone: `{Pivot:,.2f} - {R1:,.2f}` → *Potential Sell/Profit Area*
            - Fair Buy: `{Fair_Buy:,.2f}`, Fair Sell: `{Fair_Sell:,.2f}`
            - Trend Signal: **{results.loc[t, 'Trend_Signal']}**
            """)

# Run locally
if __name__ == "__main__":
    app()
