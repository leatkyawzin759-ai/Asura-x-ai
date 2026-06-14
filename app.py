import streamlit as st

st.title('Asura AI Chatbot')

# Chat history ကို သိမ်းထားဖို့
if "messages" not in st.session_state:
    st.session_state.messages = []

# အရင်ပြောထားတဲ့ message တွေကို ပြန်ပြပေးခြင်း
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ဆီက input ယူခြင်း
if prompt := st.chat_input("မင်္ဂလာပါ... ဘာများကူညီပေးရမလဲ?"):
    # User message ကို ပြသခြင်း
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chatbot ရဲ့ တုံ့ပြန်မှု (လက်ရှိမှာတော့ Echo လုပ်ထားပါတယ်)
    response = f"ညီကိုပြောလိုက်တာ - {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
  
OPENAI_API_KEY = "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"
