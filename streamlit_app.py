import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Function to get Google suggestions
def get_google_suggestions(keyword, suffixes):
    suggestions_set = set()  # Use a set to avoid duplicates
    for suffix in suffixes:
        query = f"{keyword} {suffix}"
        apiurl = f"http://suggestqueries.google.com/complete/search?output=toolbar&hl=de&q={query}"
        r = requests.get(apiurl)
        tree = ET.fromstring(r.text)
        for child in tree.iter('suggestion'):
            suggestions_set.add(child.attrib['data'])
    return sorted(suggestions_set)  # Return sorted list

# List of suffixes
suffixes = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "l", "m", "n", "o", "p", "q", "r", "s", "t", "v", "z",
            "ü", "ä", "ö", "y", "w", "x"]

# Streamlit UI
st.title("Google Search Suggestions")
st.write("This app generates Google search suggestions for a given keyword with various suffixes.")

# User input to enter a keyword
keyword = st.text_input("Enter a keyword")

if st.button("Get Suggestions"):
    if keyword.strip():
        with st.spinner("Fetching suggestions..."):
            suggestions = get_google_suggestions(keyword, suffixes)
        if suggestions:
            st.write("Suggestions (alphabetically sorted):")
            for suggestion in suggestions:
                st.write(suggestion)
            
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
    else:
        st.write("Please enter a keyword.")

if __name__ == "__main__":
    st.write("Enter a keyword and click 'Get Suggestions' to see the results.")
