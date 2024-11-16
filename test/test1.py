import streamlit as st
import time

st.set_page_config(
    page_title="チェックテストページ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初期化関数
def init():
    if "init" not in st.session_state:
        st.session_state.init = True
        reset_session()
        count()
        return True
    else:
        return False
    
# タブの状態管理
def tab_session():
    if "now_tab" not in st.session_state:
        st.session_state.now_tab = None
    if not st.session_state.now_tab == st.session_state.tab:
        reset_session()
    st.session_state.now_tab = st.session_state.tab

# レイヤーの状態管理
def layer_session(layer=0):
    st.session_state.layer = layer

# セッションをリセット
def reset_session():
    st.session_state.now_tab = None
    layer_session()

# カウンター機能
def ck():
    if "ck" not in st.session_state:
        st.session_state.ck = -1
    st.session_state.ck += 1
    return st.session_state.ck

# カウント機能
def count():
    if "count" not in st.session_state:
        st.session_state.count = 0
    st.session_state.count += 1

# デコレーター関数
def deco_horizontal(func):
    def wrapper(*args, **kwargs):
        st.write("---")
        return func(*args, **kwargs)
    return wrapper

# 戻るボタン
@deco_horizontal
def back_btn():
    st.button(f"戻る [{ck()}]", on_click=reset_session)

# 汎用ボタン
def btn(label="ボタン", key=None, onclick=None, done=None):
    if st.button(label, key=key, on_click=onclick) and done:
        done()

# popボタン機能
def pop_btn(label="pop", key=None, layer=0, onclick=lambda: None, done=None, description=None):
    placeholder = st.empty()
    with placeholder.container():
        if description:
            st.write(description)
        res = st.button(label, key=key, on_click=lambda: [placeholder.empty(), layer_session(layer), onclick()])
    if res and done:
        with placeholder:
            done()
            placeholder.empty()

# popメッセージ表示
def pop(msg, done=None, interval=1):
    with st.spinner(msg):
        time.sleep(interval)
    if done:
        done()

# Indexページ表示
def index():
    st.write("ここは **Indexページ** です。")

# サンプルコンテンツページ表示
def sample_content(i):
    st.write(f"ここは **ページ {i}** です。 [{ck()}]")
    pop_btn(
        label=f"POPボタン",
        layer=2,
        onclick=lambda: [count(), print(f"ck[{ck()}]")],
        done=lambda: [
            pop(f"POPボタンが押されました [{ck()}]"),
            st.success(f"成功！ [{ck()}]"),
            time.sleep(1)
        ]
    )

# メインコード
init()
if "ck" not in st.session_state:
    st.session_state.ck = 0

st.session_state.tab = st.sidebar.selectbox("選択してください。", ["Index", "List"])
tab_session()  # TAB切り替えの管理

# delay
time.sleep(0.1)

# タブとレイヤーによる表示制御
_tab = st.session_state.tab
_layer = st.session_state.layer if "layer" in st.session_state else 0

if _tab == "Index":
    if _layer == 0 or _layer == 1:
        layer_session(1)
        index()
elif _tab == "List":
    if _layer == 0 or _layer == 1:
        layer_session(1)
        sample_content(1)
    elif _layer == 2:
        st.info(f"POPによるページ遷移をしました。 [{ck()}]")
        sample_content(1)
        back_btn()
