"""
This is a chat interface with my digital AI clone.
"""

import streamlit as st
from gpt_index import GPTSimpleVectorIndex
import openai
import os
import streamlit.components.v1 as components

st.secrets.load_if_toml_exists()
openai.api_key = st.secrets["openai_api_key"]
openai.organization = st.secrets["openai_organization"]
assert openai.api_key is not None, "OpenAI API key not found"
os.environ["OPENAI_API_KEY"] = openai.api_key
os.environ["OPENAI_ORGANIZATION"] = openai.organization
AI_CLONE = "Jiddu Krishnamurti"

st.title(f"{AI_CLONE}'s clone")

index_path = "index.json"
# check if index exists, if not, download from public repo
if not os.path.exists(index_path):
    import requests
    url = "https://raw.githubusercontent.com/louis030195/krishnamurti-clone/main/index.json"
    r = requests.get(url, allow_redirects=True)
    open(index_path, "wb").write(r.content)
index = GPTSimpleVectorIndex.load_from_disk(index_path)
history = []

def chat(user_input: str) -> str:
    # only take last 3 messages (in practice, we should ensure it doesn't exceed the max length of the prompt)
    history_prefix = "\n---\n".join(history[-3:])
    response = index.query(f"{history_prefix}\n---\nHuman: {user_input}\n{AI_CLONE}:")
    history.append(f"Human: {user_input}\n{AI_CLONE}: {response.response}")
    return response.response

# input box
user_input = st.text_input("You", "How can I reach maximum happiness this year?")
# button
if st.button("Send"):
    # display user input
    st.write("You: " + user_input)
    # display clone response
    response = chat(user_input)
    st.write(f"{AI_CLONE}: " + response)

components.html(
    """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=primary]'));
const send = buttons.find(el => el.innerText === 'Send');
doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 13:
            send.click();
            break;
    }
});
</script>
""",
    height=0,
    width=0,
)

# add a description on how it differs from ChatGPT
# in the sense that it searches the work of Jiddu Krishnamurti
# to be used as a personality for the AI
st.markdown(
    """
    This AI clone of Jiddu Krishnamurti differs from ChatGPT in the sense that it searches the work of Jiddu Krishnamurti to be used as a personality for the AI.
    """
)

# add a warning / reminder that there a small conversation history
# of the past 3 messages that is used for the conversation
# something a nontech person understand
st.markdown(
    """
    **⚠️ Note:** The AI remembers only the past 3 messages. If you want to start a new conversation, refresh the page.
    """
)

# add a reference to the source code at https://github.com/louis030195/paul-graham-clone
st.markdown(
    """
    [Source code](https://github.com/louis030195/krishnamurti-clone)
    """
)

# reference to gpt-index
st.markdown(
    """
    Built with ❤️ by [louis030195](https://louis030195.com) using the amazing [GPT-Index](https://github.com/jerryjliu/gpt_index) library
    """
)
