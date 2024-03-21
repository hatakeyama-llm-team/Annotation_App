import streamlit as st
import authenticate as authenticate
from pages import management, annotate
from repository.user import UserRepository
from utils import Constants

# authenticate.set_st_state_vars()


def init():
    st.markdown("""
      テキストを手軽にアノテーションして品質向上するためのアプリです
                """)




    if st.button('ログインページへ'):
        st.session_state["page_control"] = Constants.LOGIN_PAGE
    elif st.button('登録ページへ'):
        st.session_state["page_control"] = Constants.REGISTER_PAGE


def login_page_show():
    st.title('ログインページ')
    user_name = st.text_input('ユーザー名')
    password = st.text_input('パスワード',type='password')
    if st.button('ログインする'):
        st.session_state["page_control"] = 1
        user_repository = UserRepository()
        is_login = user_repository.login(user_name,password)
        if is_login:
            st.write("ログインしました")
            st.session_state["user_info"] = {"name":user_name}
            st.session_state['authenticated'] = True
            st.session_state["page_control"] = Constants.ANNOTATION_PAGE
            st.spinner("読み込み中")
        else:
            st.warning("ログインできませんでした")
            st.session_state['authenticated'] = False

def register_page_show():
    st.title('登録ページ')
    user_name = st.text_input('ユーザー名')
    password = st.text_input('パスワード',type='password')
    if st.button('登録する'):
        st.write('You clicked the button')
        st.session_state["user_info"] = {"name":user_name}
        user_repository = UserRepository()
        is_register = user_repository.register(user_name,password)
        if is_register:
            st.session_state["page_control"] = Constants.ANNOTATION_PAGE
            st.write("登録しました")

        else:
            st.warning("登録できませんでした. 既に登録されているかもしれません。")
            st.session_state['authenticated'] = False

        st.spinner("読み込み中")

if __name__ == "__main__":
    st.set_page_config(page_title="アノテーションアプリ", page_icon="🐲", layout="wide",
                       )

    if 'page_control' not in st.session_state:
        st.session_state["page_control"] = Constants.MAIN_PAGE

    if st.session_state["page_control"] == Constants.MAIN_PAGE:
        init()

    elif st.session_state["page_control"] == Constants.LOGIN_PAGE:
        login_page_show()
    elif st.session_state["page_control"] == Constants.REGISTER_PAGE:
        register_page_show()

    elif st.session_state["page_control"] == Constants.ANNOTATION_PAGE:
        annotate.main()
    elif st.session_state["page_control"] == Constants.MANAGEMENT_PAGE and st.session_state['user_info']['name'] == 'admin':
        management.show()