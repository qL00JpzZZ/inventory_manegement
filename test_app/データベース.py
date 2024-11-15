import streamlit as st
from PIL import Image

st.title('データベースを表示するページ')
st.caption('在庫、メニューの一覧が見れる、操作できる')

image = Image.open('./pic/databaseImage.jpg')
st.image(image,width = 200)
