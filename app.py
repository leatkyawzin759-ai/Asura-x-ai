import streamlit as st
import base64
from groq import Groq
import requests
import io
from duckduckgo_search import DDGS

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY", "")

uploaded_file = st.file_uploader("ပုံတင်ပါ", type=['jpg', 'jpeg', 'png'])

def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')

prompt = st.chat_input("မေးခွန်းမေးပါ")

if prompt:
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        if "calculator" in prompt.lower() or "ပေါင်း" in prompt:
            st.info("🧮 Calculator ကို အသုံးပြုနိုင်ပါပြီ။")
        elif "ရှာ" in prompt or "search" in prompt.lower():
            st.write("🔍 ရှာဖွေနေပါပြီ...")
            with DDGS() as ddgs:
                results = list(ddgs.text(prompt, max_results=3))
                for r in results:
                    st.write(f"- [{r['title']}]({r['href']})")
        elif "3D" in prompt and uploaded_file:
            res = requests.post("https://api.tripo3d.ai/v2/api/task", 
                                headers={"Authorization": f"Bearer {tripo_key}"}, 
                                files={"file": uploaded_file.getvalue()})
            st.success("3D တောင်းဆိုပြီးပါပြီ။")
        elif "ပုံဆွဲ" in prompt:
            res = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", 
                                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                                files={"none": ""}, data={"prompt": prompt})
            if res.status_code == 200: st.image(io.BytesIO(res.content))
        else:
            if uploaded_file:
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
            
