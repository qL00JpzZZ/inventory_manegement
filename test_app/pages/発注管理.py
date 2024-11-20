import os
import streamlit as st
import sqlite3
import pandas as pd

st.title('材料の入荷を操作するページ')

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
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            品目 TEXT,
            賞味期限 TEXT,
            入荷日 TEXT,
            個数 INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_hacchuu_data(data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute("""
            INSERT INTO inventory (品目, 賞味期限, 入荷日, 個数)
            VALUES (?, ?, ?, ?)
        """, (entry["品目"], entry["賞味期限"], str(entry["入荷日"]), entry["個数"]))
    conn.commit()
    conn.close()

# Streamlit UI 初期化
create_tables()

















from datetime import date
# セッション状態を初期化
if "hacchuu_info" not in st.session_state:
    st.session_state["hacchuu_info"] = []
if "current_inputs" not in st.session_state:
    st.session_state["current_inputs"] = {}

# 入力データを保持するためのヘルパー関数
def update_current_inputs(kinds):
    for i in range(int(kinds)):
        st.session_state["current_inputs"][f"hacchuu_name_{i}"] = st.session_state.get(f"hacchuu_name_{i}", "")
        st.session_state["current_inputs"][f"hacchuu_expiration_{i}"] = st.session_state.get(f"hacchuu_expiration_{i}", date.today())
        st.session_state["current_inputs"][f"hacchuu_date_{i}"] = st.session_state.get(f"hacchuu_date_{i}", date.today())
        st.session_state["current_inputs"][f"hacchuu_quantity_{i}"] = st.session_state.get(f"hacchuu_quantity_{i}", 1)

# 入力フォーム
with st.form(key='hacchuu_form'):
    kinds = st.number_input('品目数', min_value=1, step=1, key='hacchuu_kinds')
    submit_button_2 = st.form_submit_button('品目数を登録')

    if submit_button_2:
        # 動的入力フィールドを初期化または保持
        update_current_inputs(kinds)

# フォーム内容の動的表示
for i in range(int(st.session_state.get('hacchuu_kinds', 1))):
    name = st.text_input(f'品目 {i + 1}', 
                         value=st.session_state["current_inputs"].get(f"hacchuu_name_{i}", ""), 
                         key=f"hacchuu_name_{i}")
    expiration_date = st.date_input(f'賞味期限 {i + 1}', 
                                    value=st.session_state["current_inputs"].get(f"hacchuu_expiration_{i}", date.today()), 
                                    key=f"hacchuu_expiration_{i}")
    arrival_date = st.date_input(f'入荷日 {i + 1}', 
                                 value=st.session_state["current_inputs"].get(f"hacchuu_date_{i}", date.today()), 
                                 key=f"hacchuu_date_{i}")
    quantity = st.number_input(f'個数 {i + 1}', 
                                value=st.session_state["current_inputs"].get(f"hacchuu_quantity_{i}", 1), 
                                min_value=1, 
                                step=1, 
                                key=f"hacchuu_quantity_{i}")

# 「データベースに登録する」ボタン
if st.button("データベースに登録"):
    for i in range(int(st.session_state.get('hacchuu_kinds', 1))):
        name = st.session_state[f"hacchuu_name_{i}"]
        expiration_date = st.session_state[f"hacchuu_expiration_{i}"]
        arrival_date = st.session_state[f"hacchuu_date_{i}"]
        quantity = st.session_state[f"hacchuu_quantity_{i}"]

        st.session_state["hacchuu_info"].append({
            "品目": name,
            "賞味期限": expiration_date,
            "入荷日": arrival_date,
            "個数": quantity
        })

    # データを挿入
    if st.session_state["hacchuu_info"]:
        insert_hacchuu_data(st.session_state["hacchuu_info"])
        st.success("発注品が登録されました！")
        st.session_state["hacchuu_info"] = []  # 登録後にリセット
        st.session_state["current_inputs"] = {}  # フォームもリセット
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

# データ表示ボタンを追加
if st.button('新規発注データを表示'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 新規発注データをSQLクエリで取得
    cursor.execute("SELECT * FROM inventory")
    hacchuu_data = cursor.fetchall()
    if hacchuu_data:
        st.write("在庫データ:")
        # データを表示
        hacchuu_df = pd.DataFrame(hacchuu_data, columns=["ID", "品目", "賞味期限", "入荷日", "個数"])
        st.write(hacchuu_df)
    else:
        st.write("在庫データはありません。")

    conn.close()
