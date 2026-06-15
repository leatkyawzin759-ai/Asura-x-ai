import streamlit as st
import base64
import requests
import io
from groq import Groq
from duckduckgo_search import DDGS
from pypdf import PdfReader
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# API Keys
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY", "")

# Input များ
audio_bytes = audio_recorder("voice", icon_size="2x")
uploaded_file = st.file_uploader("File or pdf)", type=['jpg', 'jpeg', 'png', 'pdf'])
prompt = st.chat_input("Ask Asura.")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    prompt = "အသံဖိုင်မှ အကြောင်းအရာကို ဆက်လုပ်ပေးပါ"

def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')

if prompt:
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        
        # ၁။ Calculator
        if "calculator" in prompt.lower() or "ပေါင်း" in prompt or "နှုတ်" in prompt:
            st.info("🧮 Calculator စနစ်")
            
        # ၂။ PDF Reader
        elif uploaded_file and uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in reader.pages])
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"PDF အချက်အလက်: {text[:5000]}... မေးခွန်း: {prompt}"}]
            )
            st.markdown(response.choices[0].message.content)
            
        # ၃။ Web Search
        elif "ရှာ" in prompt or "search" in prompt.lower():
            with DDGS() as ddgs:
                results = list(ddgs.text(prompt, max_results=3))
                for r in results: st.write(f"- [{r['title']}]({r['href']})")
                
        # ၄။ 3D ဖန်တီးခြင်း
        elif "3D" in prompt and uploaded_file:
            res = requests.post("https://api.tripo3d.ai/v2/api/task", 
                                headers={"Authorization": f"Bearer {tripo_key}"}, 
                                files={"file": uploaded_file.getvalue()})
            st.success("3D တောင်းဆိုမှု ပို့ပြီးပါပြီ။")
            
        # ၅။ ပုံဆွဲခြင်း
        elif "ပုံဆွဲ" in prompt:
            res = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", 
                                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                                files={"none": ""}, data={"prompt": prompt})
            if res.status_code == 200: st.image(io.BytesIO(res.content))
            
        # ၆။ AI Vision & Chat (စာရေးခြင်း/မေးခွန်းဖြေခြင်း)
        else:
            if uploaded_file and not uploaded_file.name.endswith(".pdf"):
                base64_image = encode_image(uploaded_file)
                response = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-instruct",
                    messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}]
                )
            else:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
            st.markdown(response.choices[0].message.content)
            
