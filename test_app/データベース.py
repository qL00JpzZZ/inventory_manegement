import streamlit as st
from PIL import Image
import sqlite3

st.title('データベースを表示するページ')
st.caption('在庫、メニューの一覧が見れる、操作できる')

image = Image.open('./pic/databaseImage.jpg')
st.image(image,width = 200)

#新しいメニューを登録する部分
st.caption('新しいメニューを追加')
with st.form(key = 'menu_info'):
    name = st.text_input('名前')
    kinds = st.number_input('材料の種類数',min_value = 1,step=1)
    kettei_btn = st.form_submit_button('決定')
    if kettei_btn:
        for i in range(int(kinds)):
            zairyou_key = f"zairyou_{i}"
            kosuu_key = f"kosuu_{i}"
            
            zairyou = st.text_input(f'材料名',key = zairyou_key)
            kosuu = st.number_input(f'個数',min_value = 1,step = 1,key = kosuu_key)
            
        add_btn2 = st.form_submit_button('登録')
        if add_btn2:
            st.caption('ok')


# データを SQLite に保存
conn = sqlite3.connect('メニュー')
st.session_state["data"].to_sql('your_table_name', conn, if_exists='replace', index=False)
conn.close()
st.success("データがデータベースに保存されました！")
