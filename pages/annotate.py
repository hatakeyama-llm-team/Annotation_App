import random
import streamlit as st

from repository.datasets import DataSetsRepository
from repository.evaluate_status import EvaluateStatusRepository
from streamlit_shortcuts import add_keyboard_shortcuts

from repository.user_execute_count import UserExecuteRepository


def show():
    GOOD = "良さそう😁"
    PENDING = "判断に困る🙄"
    BAD = "良くない😇"
    #
    GOOD_POINT = 100
    PENDING_POINT = 50
    BAD_POINT = 0
    # Set up the page layout
    dataset_repository = DataSetsRepository()
    try:
        dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]
    except:
        st.success("🎉全てのデータセットを評価しました！")
        st.stop()
    dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]

    user_name = ""
    if 'user_info' in st.session_state:
        user_name = st.session_state["user_info"]["name"]
        st.title(f'{user_name}さん、こんにちは！')
    evaluate_status_repository = EvaluateStatusRepository()
    user_execute_repository = UserExecuteRepository()

    fetched_user_processed_counts, fetched_all_counts,fetched_unprocessed_count = user_execute_repository.findCountByUserName(user_name)
    if fetched_user_processed_counts is None:
        fetched_user_processed_counts = 0
    if fetched_all_counts is None:
        fetched_all_counts = 0
    if fetched_unprocessed_count is None:
        fetched_unprocessed_count = 0

    user_count = st.session_state.setdefault('user_counts', fetched_user_processed_counts)
    all_count = st.session_state.setdefault('all_counts', fetched_all_counts)
    unprocessed_count = st.session_state.setdefault('unprocessed_counts', fetched_unprocessed_count)
    #
    # Add a title to the page
    st.title("AnnotateApp")
    st.markdown(
        """
    <style>
    button {
        height: 100px;
        width: 150px;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    big-font {
        font-size: 100px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    with st.expander("評価数の確認"):
        st.markdown(f"""

            すべてのデータセット数: {all_count}回

            あなたの評価数: {user_count}回

            未評価数: {unprocessed_count}回
            """)
    # Create a container for the text to be evaluated
    with st.container():

        dataset_text = dataset_repository.findOneById(dataset_id)
        st.markdown(f''
                    f'この文章を読んで評価してください'
                    )
        st.markdown(f''
                    f'{dataset_text[0]} ',
                    unsafe_allow_html=True)

    # Create two columns for 'Good' and 'Bad' buttons
    col1, col2, col3 = st.columns(3)
    add_keyboard_shortcuts({
        'Shift+A': GOOD,
    })
    add_keyboard_shortcuts({
        'Shift+S': PENDING,
    })
    add_keyboard_shortcuts({
        'Shift+D': BAD,
    })
    # Place 'Good' button in the first column
    with col1:

        if st.button(GOOD, ):
            evaluate_status_repository.insert(dataset_id, GOOD_POINT)
            st.success("ありがとうございます!")
            if user_name is not None:
                user_execute_repository.upsert(user_name)
                user_count += 1
                unprocessed_count -= 1

    with col2:

        if st.button(PENDING,
                     ):
            evaluate_status_repository.insert(dataset_id, PENDING_POINT)
            st.success("悩みますよね..!")
            if user_name is not None:
                user_execute_repository.upsert(user_name)
                user_count += 1
                unprocessed_count -= 1
    # Place 'Bad' button in the second column
    with col3:

        if st.button(BAD):
            evaluate_status_repository.insert(dataset_id, BAD_POINT)
            st.success("ありがとうございます！")
            if user_name is not None:
                user_execute_repository.upsert(user_name)
                user_count += 1
                unprocessed_count -= 1

        with st.expander("便利なショートカットキー"):
            st.markdown(f"""

                        - {GOOD}   : Shift+A
                        - {PENDING}: Shift+S
                        - {BAD}    : Shift+D

                        """)

    with st.expander("このアプリについて"):
        st.markdown("""
        CommonCrawlのデータを使って、テキストを評価するアプリです。
                    """)
    with st.expander("使い方"):
        st.markdown("""
                    1. テキストを読み込む
                    2. 読んだ文章を評価する
                    3. Good or Pending or Badを選択する
                    4. 次の文章を読み込む

                    """)
    with st.expander("Good,Pending,Badの定義"):
        st.markdown("""
                 Good/Badの例は以下の通りです。
                    - Good: 　話の筋が良い表現や、科学的根拠に基づいた表現が含まれている。
                    - Bad: R18の表現が含まれている、または、不適切な表現が含まれている。
                    - Pending: 判断に迷う

                    3. 保存する

                    """)

    st.session_state['user_counts'] = user_count
    st.session_state['all_counts'] = all_count
    st.session_state['unprocessed_counts'] = unprocessed_count
    if unprocessed_count == 0:
        st.warning("全てのデータセットを評価しました！")

if __name__ == "__main__":
    show()