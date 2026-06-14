import streamlit as st
import base64
from groq import Groq
import requests
import io

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# API Keys များကို Secrets ထဲကနေ လှမ်းခေါ်ခြင်း (ဒါမှ Key ပေါက်ကြားမှာ မဟုတ်ဘူး)
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY", "")

uploaded_file = st.file_uploader("ပုံတင်ပါ", type=['jpg', 'jpeg', 'png'])

def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')

# Chat Logic
if prompt := st.chat_input("မေးခွန်းမေးပါ (သို့) 'ပုံဆွဲ' ၊ '3D လုပ်ပေး'"):
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # ပုံတင်ထားရင် ပုံကို အရင်ဖတ်ခြင်း
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            uploaded_file.seek(0) # File pointer ကို ပြန်စခြင်း

            # 3D လုပ်ခြင်း
            if "3D" in prompt:
                st.write("ပုံကို AI မြင်နေပါပြီ... 3D စတင်လုပ်ဆောင်နေပါပြီ")
                files = {"file": uploaded_file.getvalue()}
                headers = {"Authorization": f"Bearer {tripo_key}"}
                res = requests.post("https://api.tripo3d.ai/v2/api/task", headers=headers, files=files)
                if res.status_code == 200: st.success("3D အောင်မြင်စွာ ဖန်တီးလိုက်ပါပြီ!")
                else: st.error("3D ဖန်တီးရန် API Key စစ်ဆေးပါ။")
            
            # ပုံအကြောင်း မေးခြင်း
            else:
                response = groq_client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}]
                )
                st.markdown(response.choices[0].message.content)
        
        # ပုံမပါရင် စာပဲဖြေခြင်း
        else:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown(completion.choices[0].message.content)
              
            
            
        
    
    
