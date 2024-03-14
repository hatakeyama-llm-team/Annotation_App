# common.py
import extra_streamlit_components as stx
import streamlit as st
#ログインの確認
def check_login():
    value = stx.CookieManager().get(cookie='some_cookie_name')
    if value != []:
        st.warning("**ログインしてください**")
        st.stop()
