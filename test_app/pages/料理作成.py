import streamlit as st
from PIL import Image
import sqlite3

st.title('作るメニューと個数を入力するページ')
st.caption('消費する材料の個数を計算してデータベースを編集する')
image = Image.open('./pic/sinkimenuImage.jpg')
st.image(image,width = 200)

#作る料理とその個数を入力
with st.form(key = 'ryouri_info'):
    kinds = st.number_input('料理数',min_value = 1,step=1)
    kettei_btn = st.form_submit_button('決定')
    if kettei_btn:
        for i in range(int(kinds)):
            name_key = f"name_{i}"
            kosuu_key = f"kosuu_{i}"
            
            name = st.text_input(f'料理名',key = name_key)
            kosuu = st.number_input(f'個数',min_value = 1,step = 1,key = kosuu_key)

        add_btn2 = st.form_submit_button('登録')
        if add_btn2:
            st.caption('ok')

conn = sqlite3.connect('料理作成')
st.session_state["data"].to_sql('your_table_name', conn, if_exists='replace', index=False)
conn.close()
st.success("データがデータベースに保存されました！")