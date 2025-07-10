import streamlit as st
import requests
from bs4 import BeautifulSoup

def app():
    st.title("Product Info Scraper")
    url = st.text_input("Enter product URL:", "https://example.com")

    if st.button("Scrape"):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Contoh ambil data (ganti class sesuai halaman target)
            product_name = soup.find("div", class_="product-title")
            product_rating = soup.find("div", class_="product-rating")
            product_price = soup.find("div", class_="product-price")
            product_reviews = soup.find("div", class_="product-reviews")
            purchase_timeline = soup.find("div", class_="purchase-timeline")
            st.subheader("Scraped Data:")

            st.write("**Product Name:**", product_name.get_text(strip=True) if product_name else "Not found")
            st.write("**Rating:**", product_rating.get_text(strip=True) if product_rating else "Not found")
            st.write("**Price:**", product_price.get_text(strip=True) if product_price else "Not found")
            st.write("**Reviews:**", product_reviews.get_text(strip=True) if product_reviews else "Not found")
            st.write("**Purchase Timeline:**", purchase_timeline.get_text(strip=True) if purchase_timeline else "Not found")

        except Exception as e:
            st.error(f"Error: {e}")
