import sqlite3
import streamlit as st

# データベース接続（存在しない場合は新規作成）
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# データベース内にテーブルを作成
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()

# データを挿入する関数
def insert_data(name, age):
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()

# データを取得する関数
def get_data():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Streamlit UI
st.title("SQLiteデータベース作成")

# テーブル作成
if st.button("テーブルを作成"):
    create_table()
    st.success("テーブルを作成しました！")

# データ挿入
with st.form("データ挿入"):
    name = st.text_input("商品名")
    age = st.number_input("賞味期限", min_value=0, step=1)
    submitted = st.form_submit_button("データを追加")
    if submitted:
        insert_data(name, age)
        st.success("データを追加しました！")

# データ表示
if st.button("データを表示"):
    data = get_data()
    st.write(data)

# 接続を閉じる
conn.close()