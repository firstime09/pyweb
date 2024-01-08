import streamlit as st
import numpy as np
import cv2 as cv

def app():
    st.title('Leaf Diseases Detection')
    st.markdown(
        """ In this case, we build the Machine Learning Model using two types of
            leaf diseases which are spot and blight. Details from the code and
            methods can be read in my publication list on Google Scholar
            about `Leaf Diseases Segmentation`.
        """)
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_img = cv.imdecode(file_bytes, 1)

        st.image(
            opencv_img, caption="Uploaded Image.", use_column_width=True, channels="BGR"
        )
        b,g,r = cv.split(opencv_img)
        if st.button('Diseases Area'):
            st.image(g-r)