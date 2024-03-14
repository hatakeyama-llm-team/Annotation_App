import random
import streamlit as st

from process.auth import check_login
from repository.datasets import DataSetsRepository
from repository.evaluate_status import EvaluateStatusRepository
from streamlit_shortcuts import add_keyboard_shortcuts

GOOD = "Good😁"
PENDING = "Pending🙄"
BAD = "Bad😇"

GOOD_POINT = 100
PENDING_POINT = 50
BAD_POINT = 0

evaluate_enum = {
    GOOD: GOOD_POINT,
    PENDING: PENDING_POINT,
    BAD:BAD_POINT
}

# python enum
# enum = {


def main():
    # Set up the page layout
    st.set_page_config(page_title="Annotate Data", layout="centered")
    dataset_repository = DataSetsRepository()
    dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]

    evaluate_status_repository = EvaluateStatusRepository()

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
        font-size: 200px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Create a container for the text to be evaluated
    with st.container():

        dataset_text = dataset_repository.findOneById(dataset_id)
        st.markdown(f''
                    f'この文章を読んで評価してください'
                    )
        st.markdown(f''
                    f'# {dataset_text[0]} ',
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

    with col2:

        if st.button(PENDING,
                     ):
            evaluate_status_repository.insert(dataset_id, PENDING_POINT)
            st.success("悩みますよね〜")

    # Place 'Bad' button in the second column
    with col3:

        if st.button(BAD):
            evaluate_status_repository.insert(dataset_id, BAD_POINT)
            st.success("ありがとうございます！")

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
                    - Good: このテキストは良い
                    - Pending: このテキストはどちらでもない
                    - Bad: このテキストは悪い

                    3. 保存する

                    """)



if __name__ == "__main__":
    # check_login()
    main()