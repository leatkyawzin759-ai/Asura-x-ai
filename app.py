import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. API Keys (st.secrets ထဲမှာ ထည့်ထားပေးပါ)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
STABILITY_API_KEY = st.secrets["STABILITY_API_KEY"]
TRIPO_API_KEY = st.secrets["TRIPO_API_KEY"]

groq_client = Groq(api_key=GROQ_API_KEY)

# 2. Page Setup
st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖')

# 3. Sidebar (Volume & Settings)
st.sidebar.title("Settings")
volume = st.sidebar.slider("🔊 Volume Level", 0, 100, 50)
st.sidebar.info(f"API Keys Loaded: Groq, Stability, Tripo")

# 4. Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input
if prompt := st.chat_input("Ask me anything or give a mission..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # AI Logic
        if "3d" in prompt.lower():
            response_text = f"Tripo AI mission initiated with key: {TRIPO_API_KEY[:4]}..."
        elif "image" in prompt.lower() or "ပုံဆွဲ" in prompt:
            response_text = f"Stability AI mission initiated with key: {STABILITY_API_KEY[:4]}..."
        else:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            response_text = response.choices[0].message.content
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # 6. Text-to-Speech (အသံထွက်)
        tts = gTTS(text=response_text, lang='en')
        tts.save("response.mp3")
        st.audio("response.mp3", format="audio/mp3")
        
