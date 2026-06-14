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
# 3D အတွက် Tripo Key (မရှိရင်လည်း Error မတက်အောင် စီစဉ်ထားသည်)
tripo_key = st.secrets.get("TRIPO_API_KEY", "")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ပုံတင်ရန်
uploaded_file = st.file_uploader("ပုံတင်ပါ", type=['jpg', 'jpeg', 'png'])

# Chat ပြသခြင်း
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "img" in msg: st.image(msg["img"])

if prompt := st.chat_input("မေးခွန်းမေးပါ (သို့) 'ပုံဆွဲ' ၊ '3D လုပ်ပေး'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        # ပုံဆွဲခြင်း
        if "ပုံဆွဲ" in prompt:
            res = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", 
                                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                                files={"none": ""}, data={"prompt": prompt, "output_format": "jpeg"})
            if res.status_code == 200:
                img = Image.open(io.BytesIO(res.content))
                st.image(img)
                st.session_state.messages.append({"role": "assistant", "content": "ပုံဆွဲပေးလိုက်ပါပြီ", "img": img})
            else: st.error("ပုံဆွဲ၍မရပါ။ API Key ကို စစ်ဆေးပါ။")

        # 3D လုပ်ခြင်း (အမှားကင်းအောင် စီစဉ်ထားသည်)
        elif "3D" in prompt:
            if not uploaded_file:
                st.warning("ပုံတစ်ပုံ အရင်တင်ပေးပါ။")
            elif not tripo_key:
                st.error("Tripo API Key မတွေ့ပါ။")
            else:
                st.write("3D လုပ်ဆောင်ချက်ကို စတင်နေပါပြီ...")
                # Tripo API တောင်းဆိုခြင်း
                try:
                    files = {"file": uploaded_file.getvalue()}
                    headers = {"Authorization": f"Bearer {tripo_key}"}
                    res = requests.post("https://api.tripo3d.ai/v1/image_to_3d/task", headers=headers, files=files)
                    if res.status_code == 200:
                        st.success("အောင်မြင်ပါသည်။ Tripo Dashboard တွင် ကြည့်ရှုနိုင်ပါသည်။")
                    else:
                        st.error(f"Error: {res.status_code} - API ချိတ်ဆက်မှု မမှန်ကန်ပါ။")
                except Exception as e:
                    st.error("3D ပြောင်းခြင်း မအောင်မြင်ပါ။")

        # စာဖြေခြင်း
        else:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            text = completion.choices[0].message.content
            st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})
            

                
            
                    
            
            
        
    
    
