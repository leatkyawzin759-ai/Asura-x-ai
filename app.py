import streamlit as st
import base64
from groq import Groq
import requests
import io

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# API Keys များကို Secrets မှခေါ်ခြင်း
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    stability_key = st.secrets["STABILITY_API_KEY"]
    tripo_key = st.secrets.get("TRIPO_API_KEY", "")
except:
    st.error("API Keys များ မတွေ့ရှိပါ။ Settings > Secrets တွင် ထည့်ပါ။")
    st.stop()

uploaded_file = st.file_uploader("ပုံတင်ပါ", type=['jpg', 'jpeg', 'png'])

def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')

if prompt := st.chat_input("မေးခွန်းမေးပါ (သို့) 'ပုံဆွဲ' ၊ '3D လုပ်ပေး'"):
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # ပုံတင်ထားပါက Vision သုံးခြင်း
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            uploaded_file.seek(0)

            # 3D လုပ်ခြင်း
            if "3D" in prompt:
                st.write("3D ဖန်တီးနေပါပြီ...")
                headers = {"Authorization": f"Bearer {tripo_key}"}
                files = {"file": uploaded_file.getvalue()}
                res = requests.post("https://api.tripo3d.ai/v2/api/task", headers=headers, files=files)
                if res.status_code == 200: st.success("3D ဖန်တီးမှု အောင်မြင်သည်။")
                else: st.error(f"3D Error: {res.status_code}")
            
            # ပုံကို AI က မြင်ပြီး ဖြေပေးခြင်း
            else:
                response = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-instruct",
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}]
                )
                st.markdown(response.choices[0].message.content)
        
        # ပုံမပါလျှင် စာဖြင့်သာ ဖြေခြင်း
        else:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown(completion.choices[0].message.content)
            
              
            
            
        
    
    
