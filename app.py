import streamlit as st

st.title('Asura x AI App')
st.write('အောင်မြင်စွာ တက်လာပါပြီ!')

# အောက်ပါ Code က ညီကို့ကို စာရိုက်လို့ရစေမှာပါ
name = st.text_input('မင်းနာမည်လေး ပြောပြပေးပါ')
if name:
    st.write(f'မင်္ဂလာပါ {name}! Asura AI က ကြိုဆိုပါတယ်။')
  
