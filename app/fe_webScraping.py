import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Simple Web Scraping App")

# Input URL
url = st.text_input("Enter a URL to scrape:", "https://example.com")

# Button to start scraping
if st.button("Scrape"):
    try:
        # Get page
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        page_title = soup.title.string if soup.title else "No title found"

        # Extract all h2 elements
        h2_elements = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]

        # Display results
        st.subheader("Page Title:")
        st.write(page_title)

        st.subheader("H2 Elements Found:")
        if h2_elements:
            for idx, h2 in enumerate(h2_elements, 1):
                st.write(f"{idx}. {h2}")
        else:
            st.write("No <h2> elements found.")
    except Exception as e:
        st.error(f"Error: {e}")
