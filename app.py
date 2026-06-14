import streamlit as st
from groq import Groq
import base64
import requests

st.title('Asura AI Chatbot 🤖🎨')

# API Keys
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat History ပြသခြင်း
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# User Input
if prompt := st.chat_input("မေးခွန်းမေးပါ (သို့) 'ပုံဆွဲပေး' လို့ ရိုက်ပါ"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "ပုံဆွဲ" in prompt:
            # ပုံဆွဲခြင်း
            st.write("ပုံဆွဲပေးနေပါပြီ...")
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/core",
                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                files={"none": ""},
                data={"prompt": prompt, "output_format": "jpeg"},
            )
            st.image(response.content)
            st.session_state.messages.append({"role": "assistant", "content": "ပုံဆွဲပေးလိုက်ပါပြီ", "image": response.content})
        else:
            # စာရေးခြင်း
            stream = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            
            
        
    
    
