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
            
             # အဓိက Logic အပိုင်း
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AI ဆီကို စာပို့ပြီး ဘာလုပ်ရမလဲ ဆုံးဖြတ်ခိုင်းခြင်း
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "မင်းသည် Asura App ၏ အဓိက AI Agent ဖြစ်သည်။ "
             "အသုံးပြုသူက 'App ဆောက်ပေး' လို့ ပြောရင် App အတွက် Python code ရေးပေး၊ "
             "'ပုံဆွဲ' လို့ ပြောရင် Stability API သုံး၊ '3D' လို့ ပြောရင် Tripo API သုံး။"},
            {"role": "user", "content": prompt}
        ]
    )
    # AI ရဲ့ ဆုံးဖြတ်ချက်အတိုင်း လမ်းကြောင်းပေးခြင်း
    # (အပေါ်မှာ ကျွန်တော်တို့ ရေးထားတဲ့ if/else logic တွေအတိုင်း ဆက်သွားပါမယ်)

            # --- Calculator Feature ---
if "calculator" in prompt.lower() or "ပေါင်း" in prompt or "စား" in prompt:
    st.subheader("🧮 Asura Calculator")
    col1, col2 = st.columns(2)
    num1 = col1.number_input("နံပါတ် ၁", value=0)
    num2 = col2.number_input("နံပါတ် ၂", value=0)
    
    operation = st.selectbox("လုပ်ဆောင်ချက်", ["ပေါင်း", "နှုတ်", "မြှောက်", "စား"])
    
    if st.button("တွက်ချက်မည်"):
        if operation == "ပေါင်း": result = num1 + num2
        elif operation == "နှုတ်": result = num1 - num2
        elif operation == "မြှောက်": result = num1 * num2
        elif operation == "စား": result = num1 / num2 if num2 != 0 else "Error: သုညဖြင့် မစားရ"
        st.success(f"ရလဒ်မှာ - {result}")
                        
            
        
    
    
