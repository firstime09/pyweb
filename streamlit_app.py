import streamlit as st
from multiapp import MultiApp
from app import home, fe_LEDs, try_code, fe_webScraping, fe_stockAnalytics

st.set_page_config(page_title='| fftampinongkol', page_icon='👋')
app = MultiApp()

app.add_app("My Home Page", home.app)
app.add_app("Leaf Diseases Detection", fe_LEDs.app)
app.add_app("Link Phishing Detection", try_code.app)
app.add_app("Web Scraping", fe_webScraping.app)
app.add_app("Stock Analytics", fe_stockAnalytics.app)
app.run()
