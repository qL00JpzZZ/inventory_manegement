import streamlit as st
from PIL import Image

st.title('材料の入荷を操作するページ')
image = Image.open('./pic/nyuukaImage.jpg')
st.image(image,width = 200)

#新しい材料を登録する部分
st.caption('発注した品目を登録')
with st.form(key = 'hacchuu_info'):
    kinds = st.number_input('品目数',min_value = 1,step=1)
    kettei_btn = st.form_submit_button('決定')
    if kettei_btn:
        for i in range(int(kinds)):
            name_key = f"name_{i}"
            nyuukabi_key = f"nyuukabi_{i}"
            kosuu_key = f"kosuu_{i}"
            
            name = st.text_input(f'品目',key = name_key)
            nyuukabi = st.date_input('入荷日', value=None,key = nyuukabi_key)
            kosuu = st.number_input(f'個数',min_value = 1,step = 1,key = kosuu_key)

        add_btn1 = st.form_submit_button('追加')
        if add_btn1:
            st.caption('ok')

#新しい材料を登録する部分
st.caption('新規発注の品目を登録')
with st.form(key = 'sinkihacchuu_info'):
    kinds = st.number_input('品目数',min_value = 1,step=1)
    kettei_btn = st.form_submit_button('決定')
    if kettei_btn:
        for i in range(int(kinds)):
            name_key = f"name_{i}"
            limit_key = f"limit_{i}"
            nyuukabi_key = f"nyuukabi_{i}"
            kosuu_key = f"kosuu_{i}"
            
            name = st.text_input(f'品目',key = name_key)
            limit = st.number_input(f'賞味期限',min_value = 1,step = 1,key = limit_key)
            nyuukabi = st.date_input('入荷日', value=None,key = nyuukabi_key)
            kosuu = st.number_input(f'個数',min_value = 1,step = 1,key = kosuu_key)

        add_btn2 = st.form_submit_button('登録')
        if add_btn2:
            st.caption('ok')