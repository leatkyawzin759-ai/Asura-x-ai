import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader

# API Keys
GROQ_API_KEY = "ညီကို့_GROQ_KEY_ထည့်ပါ"

groq_client = Groq(api_key=GROQ_API_KEY)

# 1. Memory စနစ်
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# Sidebar မှာ Volume Control ထည့်ခြင်း
st.sidebar.title("⚙️ Settings")
volume = st.sidebar.slider("🔊 Volume", 0, 100, 50)
st.sidebar.write(f"လက်ရှိအသံ - {volume}%")

# UI
uploaded_file = st.file_uploader("file or pdf", type=['pdf'])
prompt = st.chat_input("Ask Asura or give mission")

# အရင်ပြောခဲ့တာတွေကို ပြန်ပြရန်
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # Volume အမိန့်ကို စစ်ဆေးခြင်း
        if "volume" in prompt.lower() or "အသံ" in prompt:
            full_response = f"အသံကို {volume}% သို့ သတ်မှတ်ထားပါသည်။"
            
        elif "calculator" in prompt.lower() or "ပေါင်း" in prompt:
            full_response = "🧮 Calculator စနစ်အဆင်သင့်ရှိပါသည်။"
            
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
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
        
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
