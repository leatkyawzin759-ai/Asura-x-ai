st
import base64
from groq import Groq
import requests
import io
from PIL import Image

st.set_page_config(page_title="Asura AI Pro", page_icon="🤖")
st.title('Asura AI Pro 🤖🎮')

# API Keys များ
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]
tripo_key = st.secrets.get("TRIPO_API_KEY", "")

uploaded_file = st.file_uploader("ပုံတင်ပါ", type=['jpg', 'jpeg', 'png'])

def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')

# Chat & Logic
if prompt := st.chat_input("မေးခွန်းမေးပါ၊ 'ပုံဆွဲ'၊ '3D လုပ်ပေး' သို့မဟုတ် 'Calculator'"):
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        
        # ၁။ Calculator လုပ်ဆောင်ချက်
        if "calculator" in prompt.lower() or "ပေါင်း" in prompt or "နှုတ်" in prompt:
            st.write("🧮 Calculator ကို စတင်ပါပြီ...")
            # (ဒီနေရာမှာ Calculator UI ကို ထည့်ပါ)
            st.info("Calculator စနစ် အလုပ်လုပ်နေပါပြီ!")

        # ၂။ 3D လုပ်ဆောင်ချက်
        elif "3D" in prompt and uploaded_file:
            st.write("3D ဖန်တီးနေပါပြီ...")
            res = requests.post("https://api.tripo3d.ai/v2/api/task", 
                                headers={"Authorization": f"Bearer {tripo_key}"}, 
                                files={"file": uploaded_file.getvalue()})
            st.success("3D တောင်းဆိုမှု ပို့ပြီးပါပြီ။")

        # ၃။ ပုံဆွဲခြင်း
        elif "ပုံဆွဲ" in prompt:
            res = requests.post("https://api.stability.ai/v2beta/stable-image/generate/core", 
                                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                                files={"none": ""}, data={"prompt": prompt})
            if res.status_code == 200: st.image(io.BytesIO(res.content))

        # ၄။ AI Vision & Chat
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
            
# library ကို install လုပ်ထားပါ: pip install duckduckgo-search
from duckduckgo_search import DDGS

# Chat Logic ထဲမှာ ဒီ if condition လေး ထည့်လိုက်ပါ
        elif "ရှာ" in prompt or "search" in prompt.lower():
            st.write("🔍 အင်တာနက်ပေါ်မှာ ရှာဖွေနေပါပြီ...")
            with DDGS() as ddgs:
                results = list(ddgs.text(prompt, max_results=3))
                for r in results:
                    st.write(f"- [{r['title']}]({r['href']})")
                    st.write(r['body'])
                    
            
        
    
    
