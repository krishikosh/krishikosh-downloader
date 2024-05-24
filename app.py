import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_redirected_url(input_url):
    try:
        response = requests.get(input_url, allow_redirects=True)
        redirected_url = response.url
        return redirected_url
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def extract_and_edit_url(redirected_url):
    try:
        if '%3A' not in redirected_url:
            response = requests.get(redirected_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tag = soup.find('a', class_='dont-break-out', href=True)
            if a_tag:
                desired_url = a_tag['href']
                decoded_url = urllib.parse.unquote(desired_url)
                edited_url = decoded_url.replace('%2F', '/').replace('%3A', ':')
                start = edited_url.find('https')
                end = edited_url.find('/content') + len('/content')
                if start != -1 and end != -1:
                    final_url = edited_url[start:end]
                    return final_url
                else:
                    return "Edited URL does not match the required format."
            else:
                return "Desired element not found."
        else:
            edited_url = redirected_url.replace('%2F', '/').replace('%3A', ':')
            start = edited_url.find('https://krishikosh.egranth.ac.in/server')
            end = edited_url.find('/content') + len('/content')
            if start != -1 and end != -1:
                final_url = edited_url[start:end]
                return final_url
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Streamlit app
st.title("Krishikosh Thesis Downloader")
st.markdown("---")

input_url = st.text_input("Enter the URL:")
st.markdown("---")

if input_url:
    final_url = get_redirected_url(input_url)
    if final_url.startswith("An error occurred"):
        st.error(final_url)
    else:
        edited_url = extract_and_edit_url(final_url)
        if edited_url.startswith("An error occurred") or edited_url == "Desired element not found." or edited_url == "Edited URL does not match the required format.":
            st.error(edited_url)
        else:
            st.success(f"Thesis Download Link: [{edited_url}]({edited_url})")
