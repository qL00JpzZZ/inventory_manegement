import streamlit as st
from PIL import Image

st.title('新規メニューとその材料を登録するページ')
image = Image.open('./pic/sinkimenuImage.jpg')
st.image(image,width = 200)