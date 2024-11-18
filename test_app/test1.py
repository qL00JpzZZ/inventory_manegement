import os
import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd

st.title('材料の入荷を操作するページ')
image = Image.open('./pic/nyuukaImage.jpg')
st.image(image, width=200)

# データベースファイルのパスを指定
db_directory = "C:/zaiko/inventory_manegement/test_app"  # 保存先のディレクトリを指定
db_path = os.path.join(db_directory, "発注管理.db")  # ファイル名を「発注管理.db」に変更

# ディレクトリが存在しない場合は作成
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# データベース内にテーブルを作成
def create_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hattyuu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            arrival_date TEXT,
            quantity INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sinnkihattyuu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expiration_date INTEGER,
            arrival_date TEXT,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

# データ挿入関数
def insert_hattyuu_data(data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute("""
            INSERT INTO hattyuu (name, arrival_date, quantity)
            VALUES (?, ?, ?)
        """, (entry["品目"], str(entry["入荷日"]), entry["個数"]))
    conn.commit()
    conn.close()

def insert_sinnkihattyuu_data(data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute("""
            INSERT INTO sinnkihattyuu (name, expiration_date, arrival_date, quantity)
            VALUES (?, ?, ?, ?)
        """, (entry["品目"], entry["賞味期限"], str(entry["入荷日"]), entry["個数"]))
    conn.commit()
    conn.close()

# Streamlit UI 初期化
create_tables()

# 材料の入荷
st.caption('発注した品目を登録')
if "hacchuu_info" not in st.session_state:
    st.session_state["hacchuu_info"] = []

with st.form(key='hattyuu_form'):
    kinds = st.number_input('品目数', min_value=1, step=1)
    submit_button_1 = st.form_submit_button('発注品を登録')

    if submit_button_1:
        for i in range(int(kinds)):
            name = st.text_input(f'品目 {i + 1}', key=f"hattyuu_name_{i}")
            arrival_date = st.date_input(f'入荷日 {i + 1}', key=f"hattyuu_date_{i}")
            quantity = st.number_input(f'個数 {i + 1}', min_value=1, step=1, key=f"hattyuu_quantity_{i}")
            if name and arrival_date and quantity:
                st.session_state["hacchuu_info"].append({
                    "品目": name,
                    "入荷日": arrival_date,
                    "個数": quantity
                })

        if st.session_state["hacchuu_info"]:
            insert_hattyuu_data(st.session_state["hacchuu_info"])
            st.success("発注品が登録されました！")
            st.session_state["hacchuu_info"] = []  # 登録後にセッションをリセット

# 新規発注
st.caption('新規発注品目を登録')
if "sinkihacchuu_info" not in st.session_state:
    st.session_state["sinkihacchuu_info"] = []

with st.form(key='sinnkihattyuu_form'):
    kinds = st.number_input('品目数', min_value=1, step=1, key='sinnkihattyuu_kinds')
    submit_button_2 = st.form_submit_button('新規発注品を登録')

    if submit_button_2:
        for i in range(int(kinds)):
            name = st.text_input(f'品目 {i + 1}', key=f"sinnkihattyuu_name_{i}")
            expiration_date = st.number_input(f'賞味期限 {i + 1}', min_value=1, step=1, key=f"sinnkihattyuu_expiration_{i}")
            arrival_date = st.date_input(f'入荷日 {i + 1}', key=f"sinnkihattyuu_date_{i}")
            quantity = st.number_input(f'個数 {i + 1}', min_value=1, step=1, key=f"sinnkihattyuu_quantity_{i}")
            if name and expiration_date and arrival_date and quantity:
                st.session_state["sinkihacchuu_info"].append({
                    "品目": name,
                    "賞味期限": expiration_date,
                    "入荷日": arrival_date,
                    "個数": quantity
                })

        if st.session_state["sinkihacchuu_info"]:
            insert_sinnkihattyuu_data(st.session_state["sinkihacchuu_info"])
            st.success("新規発注品が登録されました！")
            st.session_state["sinkihacchuu_info"] = []  # 登録後にセッションをリセット

# データ表示ボタンを追加
if st.button('材料の入荷データを表示'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 材料の入荷データをSQLクエリで取得
    cursor.execute("SELECT * FROM hattyuu")
    hattyuu_data = cursor.fetchall()
    if hattyuu_data:
        st.write("材料の入荷データ:")
        # データを表示
        hattyuu_df = pd.DataFrame(hattyuu_data, columns=["ID", "品目", "入荷日", "個数"])
        st.write(hattyuu_df)
    else:
        st.write("材料の入荷データはありません。")

    conn.close()

if st.button('新規発注データを表示'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 新規発注データをSQLクエリで取得
    cursor.execute("SELECT * FROM sinnkihattyuu")
    sinnkihattyuu_data = cursor.fetchall()
    if sinnkihattyuu_data:
        st.write("新規発注データ:")
        # データを表示
        sinnkihattyuu_df = pd.DataFrame(sinnkihattyuu_data, columns=["ID", "品目", "賞味期限", "入荷日", "個数"])
        st.write(sinnkihattyuu_df)
    else:
        st.write("新規発注データはありません。")

    conn.close()
