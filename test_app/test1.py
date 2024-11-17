import sqlite3
import streamlit as st

# データベース接続（存在しない場合は新規作成）
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# データベース内にテーブルを作成
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            arrival_date TEXT,
            expiration_date TEXT
        )
    """)
    conn.commit()

# データを挿入する関数
def insert_data(name, quantity, arrival_date, expiration_date):
    cursor.execute("INSERT INTO products (name, quantity, arrival_date, expiration_date) VALUES (?, ?, ?, ?)", 
                   (name, quantity, arrival_date, expiration_date))
    conn.commit()

# データを取得する関数
def get_data():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

# Streamlit UI
st.title("SQLite データベースの管理")

# テーブル作成
if st.button("テーブルを作成"):
    create_table()
    st.success("テーブルを作成しました！")

# データ挿入
with st.form("データ挿入"):
    name = st.text_input("商品名")
    quantity = st.number_input("個数", min_value=0, step=1)
    arrival_date = st.date_input("入荷日")
    expiration_date = st.date_input("賞味期限")
    
    submitted = st.form_submit_button("データを追加")
    if submitted:
        insert_data(name, quantity, str(arrival_date), str(expiration_date))
        st.success("データを追加しました！")

# データ表示
if st.button("データを表示"):
    data = get_data()
    if data:
        st.write("登録済みのデータ:")
        st.write(data)
    else:
        st.write("データがありません")

# 接続を閉じる
conn.close()
