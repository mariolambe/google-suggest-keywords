import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Function to get Google suggestions
def get_google_suggestions(keyword, suffixes, country_code):
    suggestions_set = set()  # Use a set to avoid duplicates
    for suffix in suffixes:
        query = f"{keyword} {suffix}"
        apiurl = f"http://suggestqueries.google.com/complete/search?output=toolbar&hl={country_code}&q={query}"
        r = requests.get(apiurl)
        tree = ET.fromstring(r.text)
        for child in tree.iter('suggestion'):
            suggestions_set.add(child.attrib['data'])
    return sorted(suggestions_set)  # Return sorted list

# List of suffixes
suffixes = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n", "o", "p", "q", "r", "s", "t", "v", "z",
            "ü", "ä", "ö", "y", "w", "x"]

# Dictionary of countries and their codes
countries = {
    "Germany (de)": "de",
    "Italy (it)": "it",
    "France (fr)": "fr",
    "Spain (es)": "es",
    "United Kingdom (en)": "en",
    "United States (us)": "us",
    "Netherlands (nl)": "nl",
    "Sweden (sv)": "sv"
    # Add more countries as needed
}

# Streamlit UI
st.title("Google Search Suggestions")
st.write("This app generates Google search suggestions for a given keyword with various suffixes.")

# Form to capture user input and handle submission
with st.form(key='keyword_form'):
    keyword = st.text_input("Enter a keyword")
    country = st.selectbox("Select a country", list(countries.keys()))
    submit_button = st.form_submit_button(label='Get Suggestions')

if submit_button and keyword.strip():
    country_code = countries[country]
    with st.spinner("Fetching suggestions..."):
        suggestions = get_google_suggestions(keyword, suffixes, country_code)
    if suggestions:
        # Convert suggestions to DataFrame for download
        df = pd.DataFrame(suggestions, columns=["Suggestions"])

        # Provide download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download suggestions as CSV",
            data=csv,
            file_name='suggestions.csv',
            mime='text/csv',
        )

        # Provide copy option
        st.text_area("Suggestions (copyable)", value='\n'.join(suggestions), height=200)
    else:
        st.write("No suggestions found.")
elif submit_button:
    st.write("Please enter a keyword.")

if __name__ == "__main__":
    st.write("Enter a keyword and click 'Get Suggestions' to see the results.")
