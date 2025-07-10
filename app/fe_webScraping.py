import streamlit as st
from google_play_scraper import app as gplay_app, reviews
import pandas as pd

def app():
    st.title("Google Play Store Reviews Downloader")
    package_name = st.text_input("Enter app package name (e.g., com.whatsapp):", "com.whatsapp")

    lang_option = st.radio(
        "Select review language:",
        options=[
            ("Indonesia", "id"),
            ("English", "en")],
        format_func=lambda x: x[0])
    selected_lang = lang_option[1]
    country_option = st.radio(
        "Select country:",
        options=[("Indonesia", "id"), ("United States", "us")], format_func=lambda x: x[0])
    selected_country = country_option[1]

    review_count = st.number_input(
        "Number of reviews to fetch:",
        min_value=1,
        max_value=1000,
        value=10)

    if st.button("Fetch App Data"):
        try:
            result = gplay_app(package_name)
            st.subheader("App Information")
            st.write("**App Name:**", result["title"])
            st.write("**Rating:**", result["score"])
            st.write("**Total Reviews:**", result["reviews"])
            st.write("**Installs:**", result["installs"])

            rvs, _ = reviews(
                package_name,
                lang=selected_lang,
                country=selected_country,
                count=review_count)

            clean_reviews = []
            for rv in rvs:
                clean_reviews.append({
                    "lang": selected_lang,
                    "country": selected_country,
                    "userName": rv.get("userName", ""),
                    "score": rv.get("score", ""),
                    "content": rv.get("content", ""),
                    "at": rv.get("at", "")})

            df_reviews = pd.DataFrame(clean_reviews)

            st.subheader("Reviews")
            st.dataframe(df_reviews)

            csv = df_reviews.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Reviews as CSV",
                data=csv,
                file_name=f"{package_name}_reviews_{selected_lang}_{selected_country}.csv",
                mime="text/csv")

        except Exception as e:
            st.error(f"Error: {e}")
