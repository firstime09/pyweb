import streamlit as st
from google_play_scraper import app as gplay_app, reviews
import pandas as pd

def app():
    st.title("Google Play Store App Info + Reviews Downloader")

    package_name = st.text_input(
        "Enter app package name (e.g., com.whatsapp):",
        "com.whatsapp")

    review_count = st.number_input(
        "Number of reviews to fetch:",
        min_value=1,
        max_value=1000,
        value=10)

    if st.button("Fetch App Data"):
        try:
            # Get app info
            result = gplay_app(package_name)

            st.subheader("App Information")
            st.write("**App Name:**", result["title"])
            st.write("**Rating:**", result["score"])
            st.write("**Total Reviews:**", result["reviews"])
            st.write("**Installs:**", result["installs"])
            st.write("**Description:**", result["description"][:300] + "...")

            rvs, _ = reviews(
                package_name,
                lang='en',
                country='us',
                count=review_count)

            df_reviews = pd.DataFrame(rvs)[["userName", "score", "content", "at"]]
            st.subheader("Sample Reviews")
            st.dataframe(df_reviews)

            csv = df_reviews.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download reviews as CSV",
                data=csv,
                file_name=f"{package_name}_reviews.csv",
                mime="text/csv")

        except Exception as e:
            st.error(f"Error: {e}")
