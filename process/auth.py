import streamlit as st

def check_auth():
    if 'authenticated' not in st.session_state:
        return False
    else:
        return st.session_state['authenticated']