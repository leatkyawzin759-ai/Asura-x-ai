import streamlit as st
from groq import Groq
import requests
import io
from PIL import Image

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# API Keys
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ဖိုင်တင်ရန်နေရာ
uploaded_file = st.file_uploader("ပုံတင်ပါ (ပုံဆွဲရန် သို့မဟုတ် 3D ပြောင်းရန်)", type=['jpg', 'jpeg', 'png'])

# Chat History ပြသခြင်း
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg: st.image(msg["img"])

# User Input
if prompt := st.chat_input("ဂိမ်းအကြောင်းမေးပါ၊ 'ပုံဆွဲ' သို့မဟုတ် '3D လုပ်ပေး' ဟု ရိုက်ပါ"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. ပုံဆွဲခြင်း
        if "ပုံဆွဲ" in prompt:
            res = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", 
                                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                                files={"none": ""}, data={"prompt": prompt, "output_format": "jpeg"})
            if res.status_code == 200:
                img = Image.open(io.BytesIO(res.content))
                st.image(img)
                st.session_state.messages.append({"role": "assistant", "content": "ပုံဆွဲပေးလိုက်ပါပြီ", "img": img})
            else: st.error("ပုံဆွဲ၍မရပါ။ API Key ကို စစ်ဆေးပါ။")

        # 2. 3D Model ပြောင်းခြင်း
        elif "3D" in prompt:
            if uploaded_file and tripo_key:
                st.write("3D Model ဖန်တီးနေပါပြီ...")
                files = {"file": uploaded_file.getvalue()}
                headers = {"Authorization": f"Bearer {tripo_key}"}
                res = requests.post("https://api.tripo3d.ai/v1/image_to_3d/task", headers=headers, files=files)
                if res.status_code == 200:
                    st.success("3D ဖန်တီးမှု စတင်ပါပြီ။ Tripo Dashboard တွင် စစ်ဆေးနိုင်ပါသည်။")
                else: st.error("3D ပြောင်း၍မရပါ။")
            else: st.warning("ပုံတင်ထားခြင်းမရှိပါ သို့မဟုတ် Tripo API Key မရှိပါ။")

        # 3. ဂိမ်းအကြောင်း စာဖြေခြင်း
        else:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "မင်းသည် ဂိမ်းကျွမ်းကျင်သူဖြစ်သည်။"}] + 
                         [{"role": "user", "content": prompt}],
                stream=False
            )
            text = completion.choices[0].message.content
            st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})
                
            
                    
            
            
        
    
    
