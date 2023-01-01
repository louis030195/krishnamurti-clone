"""
This is a chat interface with my digital AI clone.
"""

import streamlit as st
from gpt_index import GPTSimpleVectorIndex
import openai
import os

st.secrets.load_if_toml_exists()
openai.api_key = st.secrets["openai_api_key"]
openai.organization = st.secrets["openai_organization"]
assert openai.api_key is not None, "OpenAI API key not found"
os.environ["OPENAI_API_KEY"] = openai.api_key
os.environ["OPENAI_ORGANIZATION"] = openai.organization
st.title("Jiddu Krishnamurti's clone")

index_path = "index.json"
# check if index exists, if not, download from public repo
if not os.path.exists(index_path):
    import requests
    url = "https://raw.githubusercontent.com/louis030195/krishnamurti-clone/main/index.json"
    r = requests.get(url, allow_redirects=True)
    open(index_path, "wb").write(r.content)
index = GPTSimpleVectorIndex.load_from_disk(index_path)

# input box
user_input = st.text_input("You", "How can I reach maximum happiness this year?")
# button
if st.button("Send"):
    # display user input
    st.write("You: " + user_input)
    # display clone response
    response = index.query(user_input)
    st.write("Louis: " + response)

