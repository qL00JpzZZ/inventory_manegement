import os
import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd

st.title('材料の入荷を操作するページ')
image = Image.open('./pic/nyuukaImage.jpg')
st.image(image, width=200)

# 保存先のディレクトリを指定
db_directory = "C:/Users/qL00J/OneDrive/zaiko/inventory_manegement/test_app/era-hanakunattakedo"  # 保存先のパス

# フォルダが存在しない場合は作成
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# セッション状態にhacchuu_infoがない場合、空のリストで初期化（フォーム外で初期化）
if "hacchuu_info" not in st.session_state:
    st.session_state["hacchuu_info"] = []

# 新しい材料を登録する部分
st.caption('発注した品目を登録')
with st.form(key='hacchuu_info_form'):
    kinds = st.number_input('品目数', min_value=1, step=1)
    kettei_btn = st.form_submit_button('決定')
    
    if kettei_btn:
        for i in range(int(kinds)):
            name_key = f"name_{i}"
            nyuukabi_key = f"nyuukabi_{i}"
            kosuu_key = f"kosuu_{i}"

            name = st.text_input(f'品目', key=name_key)
            nyuukabi = st.date_input('入荷日', value=None, key=nyuukabi_key)
            kosuu = st.number_input(f'個数', min_value=1, step=1, key=kosuu_key)

            # 辞書としてデータを格納し、セッション状態に追加
            if name and nyuukabi and kosuu:
                st.session_state["hacchuu_info"].append({"品目": name, "入荷日": nyuukabi, "個数": kosuu})

        add_btn1 = st.form_submit_button('追加')
        if add_btn1:
            st.caption('データが追加されました！')

# データを SQLite に保存
if st.session_state["hacchuu_info"]:
    db_path_hacchuu = os.path.join(db_directory, '入荷.db')  # 保存先を指定
    try:
        conn = sqlite3.connect(db_path_hacchuu)
        df_hacchuu = pd.DataFrame(st.session_state["hacchuu_info"])
        # テーブル名が指定されていない場合に 'your_table_name' を使う
        df_hacchuu.to_sql('hacchuu_table', conn, if_exists='replace', index=False)
        conn.close()
        st.success("データがデータベースに保存されました！")
    except Exception as e:
        st.error(f"データベースの保存中にエラーが発生しました: {e}")

# 新規発注の品目を登録する部分
st.caption('新規発注の品目を登録')

# セッション状態にsinkihacchuu_infoがない場合、空のリストで初期化（フォーム外で初期化）
if "sinkihacchuu_info" not in st.session_state:
    st.session_state["sinkihacchuu_info"] = []

with st.form(key='sinkihacchuu_info_form'):
    kinds = st.number_input('品目数', min_value=1, step=1)
    kettei_btn = st.form_submit_button('決定')

    if kettei_btn:
        for i in range(int(kinds)):
            name_key = f"name_{i}"
            limit_key = f"limit_{i}"
            nyuukabi_key = f"nyuukabi_{i}"
            kosuu_key = f"kosuu_{i}"

            name = st.text_input(f'品目', key=name_key)
            limit = st.number_input(f'賞味期限', min_value=1, step=1, key=limit_key)
            nyuukabi = st.date_input('入荷日', value=None, key=nyuukabi_key)
            kosuu = st.number_input(f'個数', min_value=1, step=1, key=kosuu_key)

            # 辞書としてデータを格納し、セッション状態に追加
            if name and limit and nyuukabi and kosuu:
                st.session_state["sinkihacchuu_info"].append({"品目": name, "賞味期限": limit, "入荷日": nyuukabi, "個数": kosuu})

        add_btn2 = st.form_submit_button('登録')
        if add_btn2:
            st.caption('データが登録されました！')

# データを SQLite に保存
if st.session_state["sinkihacchuu_info"]:
    db_path_sinkihacchuu = os.path.join(db_directory, '新規発注.db')  # 保存先を指定
    try:
        conn = sqlite3.connect(db_path_sinkihacchuu)
        df_sinkihacchuu = pd.DataFrame(st.session_state["sinkihacchuu_info"])
        df_sinkihacchuu.to_sql('sinkihacchuu_table', conn, if_exists='replace', index=False)
        conn.close()
        st.success("データがデータベースに保存されました！")
    except Exception as e:
        st.error(f"データベースの保存中にエラーが発生しました: {e}")
st.write("保存されるデータ: ", st.session_state["hacchuu_info"])
st.write("新規発注のデータ: ", st.session_state["sinkihacchuu_info"])
