from datetime import date
import streamlit as st
import pandas as pd
import sqlite3

# セッション状態の初期化
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["名前", "期限","入荷日","個数"])

# データの表示
st.write("現在のデータ:")
st.dataframe(st.session_state["data"])

# データ入力フォーム
with st.form("データ入力フォーム"):
    col1 = st.text_input("名前")
    col2 = st.text_input("期限")
    col3 = st.text_input("入荷日")
    col4 = st.text_input("個数")
    submitted = st.form_submit_button("登録")

    if submitted and col1 and col2:
        new_row = pd.DataFrame({"名前": [col1], "期限": [col2],"入荷日": [col3], "個数": [col4]})
        st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)
        st.session_state["data"].index = range(1, len(st.session_state["data"]) + 1)


# データを SQLite に保存
conn = sqlite3.connect('data.db')
st.session_state["data"].to_sql('your_table_name', conn, if_exists='replace', index=False)
conn.close()
st.success("データがデータベースに保存されました！")
