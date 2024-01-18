import streamlit as st
import pandas as pd
from myfunction import allFunction
from urllib.parse import urlparse

def app():
    st.title('Link Phishing Detection')
    st.markdown(
        """ In this case, we build the Machine Learning Model to detect malicious
            links like phishing or legitimate. Details from the code and methods
            can be read in my publication list on Google Scholar about
            `Link Phishing Detection`.
        """)
    url_input = st.text_input('Input The link here 👇:')
    url_lenght = len(url_input)
    url_calc = urlparse(url_input).hostname
    url_calc_www = 1 if url_calc and 'www' in url_calc.lower() else 0
    url_calc_com = 1 if url_calc and '.com' in url_calc.lower() else 0
    url_host_lenght = len(urlparse(url_input).netloc)
    if url_lenght == 0:
        st.write(0)
    else:
        url_link_ratio = sum(char.isdigit() for char in url_input)
        url_link_ratio = (url_link_ratio/len(url_input))

        url_host_ratio = sum(char.isdigit() for char in url_calc)
        url_host_ratio = (url_host_ratio/len(url_calc))
        # st.write(url_link_ratio/len(url_input))
        # st.write(url_host_ratio/len(url_calc))
        # print(url_link_ratio / len(url_input))
        fe_list = [url_calc_www, url_calc_com, url_lenght, url_host_lenght, url_link_ratio, url_host_ratio]
        st.write(fe_list)
    # url_host_ratio = url_link_ratio/url_host_lenght
    # st.write(url_link_ratio)
    # st.write(url_host_ratio)

    st.markdown('''wait for the next update...''')