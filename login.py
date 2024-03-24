import streamlit as st
from dotenv import load_dotenv

from pages import annotate, management
from repository.cloud_sql_mysql.user import UserRepository
from utils import Constants


def change_to_annotate(user_name, password):
    st.session_state['authenticated'] = True
    st.session_state["user_info"] = {"name": user_name}
    user_repository = UserRepository()
    is_login = user_repository.login(user_name, password)
    if is_login:
        st.write("ログインしました")
        st.session_state['authenticated'] = True
        st.session_state["page_control"] = Constants.ANNOTATION_PAGE

    else:
        st.session_state['authenticated'] = False
        st.session_state['page_control'] =Constants.LOGIN_PAGE


def login_page_show():
    st.title('ログインページ')

    with st.form('login_form'):
        user_name = st.text_input('ユーザー名')
        password = st.text_input('パスワード', type='password')
        st.form_submit_button('ログインする',
                              on_click=change_to_annotate(user_name, password))

def handle_regist_user(user_name,password):
    st.session_state["user_info"] = {"name": user_name}
    user_repository = UserRepository()
    is_register = user_repository.register(user_name, password)
    if is_register:
        st.session_state["page_control"] = Constants.ANNOTATION_PAGE
        st.write("登録しました")

    else:
        st.warning("登録できませんでした. 既に登録されているかもしれません。")
        st.session_state['authenticated'] = False


def register_page_show():
    st.title('登録ページ')

    with st.form('register_form'):
        user_name = st.text_input('ユーザー名')
        password = st.text_input('パスワード', type='password')
        st.form_submit_button('登録する',on_click=handle_regist_user(user_name,password))

def main():
    load_dotenv('.env')
    st.set_page_config(page_title="アノテーションアプリ", page_icon="🐲", layout="wide",
                       initial_sidebar_state="collapsed"
                       )

    if 'page_control' not in st.session_state:
        st.session_state["page_control"] = Constants.MAIN_PAGE

    if st.session_state["page_control"] == Constants.MAIN_PAGE:
        st.markdown("""
          テキストを手軽にアノテーションして品質向上するためのアプリです
                    """)

        login_page_show()

        if st.button('登録ページへ'):
            st.session_state["page_control"] = Constants.REGISTER_PAGE

    elif st.session_state["page_control"] == Constants.LOGIN_PAGE:
        login_page_show()
    elif st.session_state["page_control"] == Constants.REGISTER_PAGE:
        register_page_show()

    elif st.session_state["page_control"] == Constants.ANNOTATION_PAGE:
        annotate.main()
    elif st.session_state["page_control"] == Constants.MANAGEMENT_PAGE and st.session_state['user_info'][
        'name'] == 'admin':
        management.show()


if __name__ == "__main__":
    main()
