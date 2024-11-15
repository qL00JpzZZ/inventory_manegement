import streamlit as st
from PIL import Image

st.title('材料の入荷を操作するページ')
image = Image.open('./pic/nyuukaImage.jpg')
st.image(image,width = 200)