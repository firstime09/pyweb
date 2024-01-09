import streamlit as st
from multiapp import MultiApp
from app import home, fe_LEDs, fe_LIPs

st.set_page_config(page_title='| fftampinongkol', page_icon='👋')
apps = MultiApp()

apps.add_app("My Home Page", home.app)
apps.add_app("Leaf Diseases Detection", fe_LEDs.app)
apps.run()
