import streamlit as st
import pandas as pd
import yfinance as yf
from app import myfunction as mf

stockAnalytics = mf.allFunction.calc_levels_with_fair_value
tickers = ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"]
data = yf.download(tickers, start="2025-08-08", end="2025-10-07", group_by='ticker')

def app():
    st.title('Stock Analysis')
    st.markdown(""" In this study, we develop a stock analysis model that utilizes the Support and Resistance approach to identify potential
        entry and exit zones while confirming price movement strength through volume analysis. The methodology, code implementation, and
        data processing details — including historical price retrieval, pivot-based level computation (S1–R2), volume confirmation, and
        fair value estimation for buy/sell decisions — are thoroughly explained in my publication list and supporting materials available
        on Google Scholar under the topic “Stock Analysis Using Support and Resistance”.
        """)

    results = pd.DataFrame({t: stockAnalytics(data[t]) for t in tickers}).T
    print("\n=== SUPPORT, RESISTANCE, VOLUME & FAIR VALUE ANALYSIS ===")
    print(results[['Pivot', 'S1', 'R1', 'Fair_Buy', 'Fair_Sell', 'Trend_Signal']])
