import streamlit as st
from groq import Groq

st.title('Asura Groq Chatbot')

# Groq client ကို ခေါ်ခြင်း (Secrets ထဲက KEY ကို GROQ_API_KEY လို့ ပြောင်းထည့်ပါ)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("မင်္ဂလာပါ..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Groq model ကို သုံးခြင်း (ဥပမာ - llama3-8b-8192)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    
