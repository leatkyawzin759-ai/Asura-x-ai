import streamlit as st
from groq import Groq

st.title('Asura Groq Chatbot')

# API Key ကို လုံခြုံစွာခေါ်ယူခြင်း
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("API Key မတွေ့ရှိပါ။ Streamlit Secrets တွင် GROQ_API_KEY ကို စစ်ဆေးပါ။")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("မင်္ဂလာပါ..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        st.error(f"Error ဖြစ်သွားပါတယ်: {e}")
        
    
    
