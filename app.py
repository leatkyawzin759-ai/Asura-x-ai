import streamlit as st
from groq import Groq
import requests
import io
from PIL import Image
import time

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖🕹️")
st.title('Asura AI Pro 🤖🎮')

# API Keys လုံခြုံစွာခေါ်ယူခြင်း
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY") # 3D API Key

# System Message (AI ရဲ့ စရိုက်)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "မင်းက ဂိမ်းလောကရဲ့ ကျွမ်းကျင်သူဖြစ်တယ်။ ညီကိုတင်တဲ့ပုံတွေကို ရှင်းပြနိုင်သလို၊ ပုံဆွဲပေးခြင်း၊ 3D Model နှင့် ဗီဒီယို ဖန်တီးခြင်းဆိုင်ရာ အကြံဉာဏ်များ ပေးနိုင်သူဖြစ်သည်။"}]

# ဖိုင်တင်ရန်နေရာ (ပုံရိပ်ကို 3D ပြောင်းရန်)
uploaded_file = st.file_uploader("ပုံတင်ပြီး 3D ပြောင်းရန်", type=['jpg', 'jpeg', 'png'])

# Chat History ပြသခြင်း
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"])
            if "3d_model" in message:
                st.write("3D Model ဖန်တီးပြီးပါပြီ။ အောက်ပါလင့်ခ်တွင် Download ရယူပါ -")
                st.markdown(f"[Download .GLB Model]({message['3d_model']})")

# User Input
if prompt := st.chat_input("ဂိမ်းအကြောင်းမေးပါ (သို့) 'ပုံဆွဲပေး' ၊ '3D လုပ်ပေး' ဟု ရိုက်ပါ"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. 3D Model ဖန်တီးခြင်း
        if "3D" in prompt:
            if not uploaded_file:
                st.error("3D ပြောင်းရန် ပုံတစ်ပုံကို အရင်တင်ပေးပါ။")
            elif not tripo_key:
                st.error("Tripo API Key ကို Secrets ထဲမှာ မတွေ့ပါ။")
            else:
                st.write("3D Model ဖန်တီးနေပါပြီ (အနည်းငယ် ကြာနိုင်ပါတယ်)...")
                # Step 1: Upload image to Tripo
                files = {"file": uploaded_file.getvalue()}
                headers = {"Authorization": f"Bearer {tripo_key}"}
                
                # Tripo API သို့ ပုံပို့ခြင်း
                upload_response = requests.post("https://api.tripo3d.ai/v1/image_to_3d/task", headers=headers, files=files)
                task_id = upload_response.json().get("data", {}).get("task_id")

                if task_id:
                    # Step 2: Check status (Polling)
                    while True:
                        time.sleep(5)
                        status_response = requests.get(f"https://api.tripo3d.ai/v1/task/{task_id}", headers=headers)
                        task_data = status_response.json().get("data", {})
                        status = task_data.get("status")

                        if status == "success":
                            model_url = task_data.get("output", {}).get("glb")
                            st.write("3D Model အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ!")
                            st.markdown(f"[Download .GLB Model]({model_url})")
                            st.session_state.messages.append({"role": "assistant", "content": "3D Model ဖန်တီးပြီးပါပြီ", "3d_model": model_url})
                            break
                        elif status == "failed":
                            st.error("3D Model ဖန်တီးခြင်း မအောင်မြင်ပါ။")
                            break
                else:
                    st.error("Tripo API သို့ ပုံပို့ခြင်း မအောင်မြင်ပါ။")

        # 2. ပုံဆွဲခြင်း
        elif "ပုံဆွဲ" in prompt:
            st.write("ပုံဆွဲပေးနေပါပြီ...")
            # Stability AI API call (ယခင်အတိုင်း)
            response = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"}, files={"none": ""}, data={"prompt": prompt, "output_format": "jpeg"})
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                st.image(image)
                st.session_state.messages.append({"role": "assistant", "content": "ပုံဆွဲပေးလိုက်ပါပြီ", "image": image})
            else:
                st.error("ပုံဆွဲ၍မရပါ။")

        # 3. စကားပြောခြင်း (Gaming Expert)
        else:
            stream = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages], stream=True)
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
                    
            
            
            
            
            
            
        
    
    
