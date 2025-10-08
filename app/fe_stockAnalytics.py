import streamlit as st
import yfinance as yf

def app():
    st.title('Stock Analysis')
    st.markdown(""" In this study, we develop a stock analysis model that utilizes the Support and Resistance approach to identify potential
        entry and exit zones while confirming price movement strength through volume analysis. The methodology, code implementation, and
        data processing details — including historical price retrieval, pivot-based level computation (S1–R2), volume confirmation, and
        fair value estimation for buy/sell decisions — are thoroughly explained in my publication list and supporting materials available
        on Google Scholar under the topic “Stock Analysis Using Support and Resistance.”.
        """)
    cols = st.columns([1, 3])
