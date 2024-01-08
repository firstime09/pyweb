import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, func):
        self.apps.append({"title":title, "function":func})
    def run(self):
        st.sidebar.header('My Prototipe List')
        app = st.sidebar.selectbox('Choose what you want to try:', self.apps,
                           format_func=lambda app: app['title'])
        app['function']()