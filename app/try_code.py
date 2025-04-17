import pickle as pk
import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from app import myfunction as mf

url_lenght = mf.allFunction.calculate_url_length
url_calc_www = mf.allFunction.calculate_www
url_calc_com = mf.allFunction.calculate_com
url_host_lenght = mf.allFunction.calculate_hostname_length
url_calc_ratio = mf.allFunction.calculate_ratio_digits
out_link = mf.allFunction.output_link

def app():
    st.title('Link Phishing Detection')
    st.markdown(
        """ In this case, we build the Machine Learning Model to detect malicious
            links like phishing or legitimate. Details from the code and methods
            can be read in my publication list on Google Scholar about
            `Link Phishing Detection`.
        """)
    ##model = mf.allFunction.load_model('m00_rf_mean_acc87p.pkl')[2]
    model = mf.allFunction.load_model('/content/m2_rf_mean_acc76p_withScale.pkl')[2]

    url_input = st.text_input('Input The link here 👇:')
    if st.button('Check Link'):
        if not url_input:
            st.warning('Input link first')
        else:
            f1 = [url_calc_www(url_input)]
            f2 = [url_calc_com(url_input)]
            f3 = [url_lenght(url_input)]
            f4 = [url_host_lenght(url_input)]
            f5 = [url_calc_ratio(url_input)]
            f6 = [url_calc_ratio(urlparse(url_input).netloc)]
            ndt = pd.DataFrame({'nb_www': f1, 'nb_com': f2, 'length_url': f3,
                            'length_hostname': f4, 'ratio_digits_url': f5,
                            'ratio_digits_host': f6})
            
            pred_rf = model.predict(ndt)
            st.warning(out_link(pred_rf, url_input))
