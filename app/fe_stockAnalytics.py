import streamlit as st
import yfinance as yf
from app import myfunction as mf

stockAnalytics = mf.calc_levels_with_fair_value

def app():
    st.title('Stock Analysis')
    st.markdown(""" In this study, we develop a stock analysis model that utilizes the Support and Resistance approach to identify potential
        entry and exit zones while confirming price movement strength through volume analysis. The methodology, code implementation, and
        data processing details — including historical price retrieval, pivot-based level computation (S1–R2), volume confirmation, and
        fair value estimation for buy/sell decisions — are thoroughly explained in my publication list and supporting materials available
        on Google Scholar under the topic “Stock Analysis Using Support and Resistance”.
        """)
cols = st.columns([1, 3])
    
DEFAULT_STOCKS = ["BBRI.JK", "BBCA.JK", "BMRI.JK", "BBNI.JK"]
if "tickers_input" not in st.session_state:
    st.session_state.tickers_input = st.query_params.get("stocks", ",".join(DEFAULT_STOCKS)).split(",")
