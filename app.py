import streamlit as st
from groq import Groq
import requests
import io
from PIL import Image

st.set_page_config(page_title="Asura AI", page_icon="🤖")
st.title('Asura AI Chatbot 🤖🎨')

# API Keys
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
stability_key = st.secrets["STABILITY_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "မင်းက ဂိမ်းလောကရဲ့ ကျွမ်းကျင်သူ (Gaming Expert) ဖြစ်တယ်။"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"])

if prompt := st.chat_input("Ask Asura"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "ပုံဆွဲ" in prompt:
            st.write("Creating your image...")
            safe_prompt = f"A high quality illustration of: {prompt}"
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/core",
                headers={"authorization": f"Bearer {stability_key}", "accept": "image/*"},
                files={"none": ""},
                data={"prompt": safe_prompt, "output_format": "jpeg"},
            )
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                st.image(image)
                st.session_state.messages.append({"role": "assistant", "content": "ပုံဆွဲပေးလိုက်ပါပြီ", "image": image})
            else:
                st.error("ပုံဆွဲ၍မရပါ။")
        else:
            # stream=False လုပ်လိုက်တာမို့လို့ JSON တွေ ပေါ်မလာတော့ပါဘူး
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=False, 
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            
            
            
            
            
            
        
    
    
