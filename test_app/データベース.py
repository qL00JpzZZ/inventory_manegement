import streamlit as st
import sqlite3
import pandas as pd

st.title('データベースを表示するページ')
st.caption('在庫、メニューの一覧が見れる、操作できる')

# データベースファイルのパス
db_path = "C:/zaiko/inventory_manegement/test_app/発注管理.db"  # 発注管理.pyで使用しているデータベースと同じパス

# データベース接続
def fetch_data(query):
    conn = sqlite3.connect(db_path)
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# 材料の入荷データを表示
try:
    hattyuu_data = fetch_data("SELECT * FROM hattyuu")
    if not hattyuu_data.empty:
        st.write("材料の入荷データ:")
        st.dataframe(hattyuu_data)
    else:
        st.write("材料の入荷データはありません。")
except Exception as e:
    st.error(f"材料の入荷データ取得時にエラーが発生しました: {e}")

# 新規発注データを表示
try:
    sinnkihattyuu_data = fetch_data("SELECT * FROM sinnkihattyuu")
    if not sinnkihattyuu_data.empty:
        st.write("新規発注データ:")
        st.dataframe(sinnkihattyuu_data)
    else:
        st.write("新規発注データはありません。")
except Exception as e:
    st.error(f"新規発注データ取得時にエラーが発生しました: {e}")

# 新しいメニューを登録
st.caption('新しいメニューを追加')
if "menu_info" not in st.session_state:
    st.session_state["menu_info"] = []

with st.form(key='menu_form'):
    menu_name = st.text_input('メニュー名')
    num_ingredients = st.number_input('材料の種類数', min_value=1, step=1)
    submit_menu = st.form_submit_button('材料を入力')

    if submit_menu:
        for i in range(int(num_ingredients)):
            ingredient_name = st.text_input(f'材料名 {i + 1}', key=f"ingredient_name_{i}")
            ingredient_qty = st.number_input(f'必要個数 {i + 1}', min_value=1, step=1, key=f"ingredient_qty_{i}")
            if ingredient_name and ingredient_qty:
                st.session_state["menu_info"].append({
                    "材料名": ingredient_name,
                    "必要個数": ingredient_qty
                })

        if st.session_state["menu_info"]:
            # メニュー情報をデータベースに保存（仮に「menu」というテーブルを使用）
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS menu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        ingredient TEXT,
                        quantity INTEGER
                    )
                """)
                for item in st.session_state["menu_info"]:
                    cursor.execute("""
                        INSERT INTO menu (name, ingredient, quantity)
                        VALUES (?, ?, ?)
                    """, (menu_name, item["材料名"], item["必要個数"]))
                conn.commit()
                conn.close()
                st.success("メニューが登録されました！")
                st.session_state["menu_info"] = []  # 登録後にセッションをリセット
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
