import streamlit as st
from process.auth import check_auth
from repository.datasets import DataSetsRepository
from repository.user_execute_count import UserExecuteRepository
from repository.evaluate_status import EvaluateStatusRepository
from utils import Constants  # GOOD, PENDING, BAD などの定数を含む外部ファイル
from streamlit_shortcuts import add_keyboard_shortcuts


def fetch_dataset(dataset_id, dataset_text):
    try:
        st.session_state['dataset_id'] = dataset_id
        st.session_state['dataset_text'] = dataset_text
    except IndexError:
        st.success("🎉全てのデータセットを評価しました！")
        st.stop()
def initialize_session_state():
    user_execute_repository = UserExecuteRepository()
    dataset_repository = DataSetsRepository()
    if 'user_counts' not in st.session_state:
        st.session_state['user_counts'] = \
        user_execute_repository.findCountByUserName(st.session_state.get('user_name'))[0]
    if 'all_counts' not in st.session_state:
        st.session_state['all_counts'] = (
            user_execute_repository.findCountByUserName(st.session_state.get('user_name')))[1]
    if 'unprocessed_counts' not in st.session_state:
        st.session_state['unprocessed_counts'] = user_execute_repository.findCountByUserName(st.session_state.get('user_name'))[2]

    if 'evaluate_point' not in st.session_state:
        st.session_state['evaluate_point'] = 0
    if 'dataset_id' not in st.session_state:
        st.session_state['dataset_id'] = dataset_repository.randomChoiseIdByUnprocessed()[0]
    if 'dataset_text' not in st.session_state:
        st.session_state['dataset_text'] = dataset_repository.findOneById(st.session_state.get('dataset_id'))[0]
def display_sidebar():
    user_info = st.session_state.get('user_info')
    st.sidebar.title(f"{user_info.get('name')}さん,こんにちは！")
    with st.expander("評価数の確認", expanded=True):
        st.sidebar.markdown(f"""
            ```
            
            評価数の確認
            
            すべてのデータセット数: {st.session_state.get('all_counts')}回

            あなたの評価数: {st.session_state.get('user_counts')}回

            未評価数: {st.session_state.get('unprocessed_counts')}回
            ```
            """)

    with st.expander("便利なショートカットキー"):
        st.sidebar.markdown(Constants.SHORTCUTS)

def display_instructions():
        st.sidebar.markdown(Constants.INSTRUCTIONS)

def evaluate_text():
    st.info('## Q1.次の文章を読んで評価してください。')

    st.markdown(f"**ヘッダー**\n\n{st.session_state.get('dataset_text')[:100]}\n\n**内容**\n"
                f"\n{st.session_state.get('dataset_text')[100:200]}\n"
                f"\n**フッター**\n\n{st.session_state.get('dataset_text')[200:300]}")

def handle_evaluation(evaluation_point):
    st.session_state['evaluate_point'] = evaluation_point

def form_field_with_placeholder(form, label ):
    st.info('## Q2.次の意味をなす文章に修正して下さい。')
    feedback_text = st.text_area(label, value=st.session_state.get('dataset_text'), key=label,height=220)
    st.session_state['feedback_text'] = feedback_text


def show_evaluation_buttons():
    evaluate_point = None
    col1,col2, col3 = st.columns(3)
    with col1:
        if st.button(Constants.GOOD):
            evaluate_point = Constants.GOOD_POINT
    with col2:
        if st.button(Constants.PENDING):
            evaluate_point = Constants.PENDING_POINT
    with col3:
        if st.button(Constants.BAD):
            evaluate_point = Constants.BAD_POINT
    st.session_state['evaluate_point'] = evaluate_point



def submit_feedback( user_execute_repository, evaluate_status_repository):

    if st.session_state.get('is_submit'):
        fetch_dataset(st.session_state.get('dataset_id'), st.session_state.get('dataset_text'))

        dataset_repository = DataSetsRepository()
        dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]
        dataset_text = dataset_repository.findOneById(dataset_id)[0]

        st.session_state['dataset_id'] = dataset_id
        st.session_state['dataset_text'] = dataset_text
        st.session_state['user_counts'] += 1
        st.session_state['unprocessed_counts'] -= 1
        evaluate_status_repository.insert(st.session_state.get('dataset_id'),
                                          st.session_state.get('evaluate_point'),
                                          st.session_state.get('feedback_text'),
                                          ''
                                        ),
        user_execute_repository.upsert(st.session_state.get('user_name'))

        st.success("修正した文章と評価を送信しました！")
        # データセットとセッションステートを更新

def set_styling():
    st.markdown(
        """
    <style>
    big-font {
        font-size: 30px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

def main():
    if not check_auth():
        st.warning("ログインしてください")
        return
    set_styling()
    initialize_session_state()

    user_execute_repository = UserExecuteRepository()
    evaluate_status_repository = EvaluateStatusRepository()
    display_sidebar()

    display_instructions()
    evaluate_text()

    show_evaluation_buttons()
    form = st.form(key='my_form')
    is_submit = form.form_submit_button('送信')
    st.session_state['is_submit'] = is_submit
    form_field_with_placeholder(form, "修正した文章")
    submit_feedback(user_execute_repository, evaluate_status_repository)

    # 他の評価処理やフォームの処理など

if __name__ == "__main__":
    main()
