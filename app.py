import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="Asura AI", page_icon="🤖")
st.title('Asura AI Chatbot 🤖')

# API Key ကို Secrets ထဲကနေ ခေါ်ယူခြင်း
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key မတွေ့ရှိပါ။ Streamlit Settings > Secrets ထဲတွင် GROQ_API_KEY ထည့်ပေးပါ။")
    st.stop()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Message များကို ပြသခြင်း
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("ဘာများ ကူညီပေးရမလဲ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Groq AI Model ကို ခေါ်ခြင်း
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error ဖြစ်သွားပါတယ်: {e}")
            
            
        
    
    
