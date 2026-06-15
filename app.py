import streamlit as st
import base64
import requests
import io
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader

# API Keys (ညီကို့ Key တွေကို ဒီနေရာမှာ ထည့်ပါ)
GROQ_API_KEY = "ညီကို့_GROQ_KEY_ကို_ဒီမှာထည့်ပါ"
STABILITY_API_KEY = "ညီကို့_STABILITY_KEY_ကို_ဒီမှာထည့်ပါ"
TRIPO_API_KEY = "ညီကို့_TRIPO_KEY_ကို_ဒီမှာထည့်ပါ"

groq_client = Groq(api_key=GROQ_API_KEY)

# 1. Memory စနစ်
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# UI
uploaded_file = st.file_uploader("ဖိုင်တင်ရန် (ပုံ/PDF)", type=['jpg', 'jpeg', 'png', 'pdf'])
prompt = st.chat_input("မေးခွန်းမေးပါ (သို့) စာရေးခိုင်းပါ...")

# အရင်ပြောခဲ့တာတွေကို ပြန်ပြရန်
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    # 2. User input ကို သိမ်းရန်
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # Logic အပိုင်းများ
        if "calculator" in prompt.lower() or "ပေါင်း" in prompt:
            full_response = "🧮 Calculator စနစ်အလုပ်လုပ်နေပါသည်။ ဘာကို တွက်ပေးရမလဲ?"
        
        elif uploaded_file and uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in reader.pages])
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"PDF အချက်အလက်: {text[:5000]}... မေးခွန်း: {prompt}"}]
            )
            full_response = response.choices[0].message.content
            
        elif "ရှာ" in prompt or "search" in prompt.lower():
            with DDGS() as ddgs:
                results = list(ddgs.text(prompt, max_results=3))
                full_response = "ရှာဖွေတွေ့ရှိချက်များ:\n" + "\n".join([f"- [{r['title']}]({r['href']})" for r in results])
        
        else:
            # 3. AI မှ မှတ်မိပြီး ဖြေပေးခြင်း
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
        
        st.markdown(full_response)
        # 4. AI အဖြေကို သိမ်းရန်
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
