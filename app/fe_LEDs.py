import streamlit as st
import numpy as np
import cv2, pywt

def app():
    st.title('Leaf Diseases Detection')
    st.markdown(
        """ In this case, we build the Machine Learning Model using two types of
            leaf diseases which are spot and blight. Details from the code and
            methods can be read in my publication list on Google Scholar
            about `Leaf Diseases Segmentation`.
        """)
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])
    col1, col2 = st.columns(2)
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        b,g,r = cv2.split(opencv_img)
        gr = g-r
        hitdwt = pywt.dwt2(gr, "db2")
        LL, (LH, HL, HH) = hitdwt
        
        col1.image(opencv_img, caption="Uploaded Image.", channels="BGR")
        col2.image(gr, caption="Diseases Areas.")
    