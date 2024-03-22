import streamlit as st

from login import login_page_show
from process.auth import check_auth
from repository.datasets import DataSetsRepository
from repository.user_execute_count import UserExecuteRepository
from repository.evaluate_status import EvaluateStatusRepository
from utils import Constants  # GOOD, PENDING, BAD などの定数を含む外部ファイル
def fetch_dataset(dataset_id, dataset_text):
    try:
        st.session_state['dataset_id'] = dataset_id
        st.session_state['dataset_text'] = dataset_text
    except IndexError:
        st.success("🎉全てのデータセットを評価しました！")
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
    if 'q1_answered' not in st.session_state:
        st.session_state['q1_answered'] = False
    if 'is_submit' not in st.session_state:
        st.session_state['is_submit'] = False
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
    with st.expander("### Q1.次の文章を読んで評価してください", expanded=False):
        st.markdown(f'''
            【定義】
            1. **ヘッダー**：文章の冒頭部分。文章の0文字目から100文字目までの部分
            2. **内容**：文章の中心部分。文章の100文字目から200文字目までの部分
            3. **フッター**：文章の終わり部分。文章の200文字目から300文字目までの部分
            
            【評価基準】
            
            次の評価基準に従って評価してください。
            
            1. {Constants.GOOD}：ヘッダー、内容、フッター３つすべてをつなげた文章が意味をなしている場合
            2. {Constants.PENDING}：ヘッダー、内容、フッターのうち、１つまたは２つ意味をなしているかどうか不明な場合
            3. {Constants.BAD}：ヘッダー、内容、フッターをつなげた文章が意味をなしていない場合
            
            ''')

    st.markdown(f"**ヘッダー**\n\n{st.session_state.get('dataset_text')[:100]}\n\n**内容**\n"
                f"\n{st.session_state.get('dataset_text')[100:200]}\n"
                f"\n**フッター**\n\n{st.session_state.get('dataset_text')[200:300]}")


def handle_evaluation(evaluation_point):
    st.session_state['evaluate_point'] = evaluation_point

def form_field_with_placeholder( label ):
    with st.expander("Q2.次の文章を、意味をなす文章に修正して下さい", expanded=False):
        st.markdown(f'''
            意味をなす文章にしてください。
            全く意味をなさない文章の場合：全選択して削除してください。
        ''')
    feedback_text = st.text_area(label, value=st.session_state.get('dataset_text'), key=label,height=220)
    st.session_state['feedback_text'] = feedback_text


def show_evaluation_buttons():
    col1,col2, col3 = st.columns(3)
    with col1:
        if st.button(Constants.GOOD,on_click=handle_evaluation_callback):
            evaluate_point = Constants.GOOD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col2:
        if st.button(Constants.PENDING,on_click=handle_evaluation_callback):
            evaluate_point = Constants.PENDING_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')

    with col3:
        if st.button(Constants.BAD,on_click=handle_evaluation_callback):
            evaluate_point = Constants.BAD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')

from streamlit_shortcuts import add_keyboard_shortcuts


def handle_evaluation_callback():
    st.session_state['q1_answered'] = True
def add_shortcut():
    add_keyboard_shortcuts({'Shift+A': Constants.GOOD})
    add_keyboard_shortcuts({'Shift+S':Constants.PENDING})
    add_keyboard_shortcuts({'Shift+D':Constants.BAD})

def submit_feedback():
    user_execute_repository = UserExecuteRepository()
    evaluate_status_repository = EvaluateStatusRepository()
    dataset_repository = DataSetsRepository()

    if st.button('次の文章を評価する') and st.session_state['q1_answered']:
        st.session_state['user_counts'] += 1
        st.session_state['unprocessed_counts'] -= 1
        evaluate_status_repository.insert(st.session_state.get('dataset_id'),
                                          st.session_state.get('evaluate_point'),
                                          st.session_state.get('feedback_text'),
                                          ''
                                        ),
        user_execute_repository.upsert(st.session_state.get('user_name'))
        st.session_state['dataset_id'] = dataset_repository.randomChoiseIdByUnprocessed()[0]
        st.session_state['dataset_text'] = dataset_repository.findOneById(st.session_state.get('dataset_id'))[0]
        st.session_state['q1_answered'] = False

        st.write('回答ありがとうございます！')
        initialize_session_state()



    else:
        if st.session_state.get('q1_answered') == False:
            st.warning('Q1が未回答です。Q1に回答お願いします')




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
        login_page_show()
        return
    set_styling()
    initialize_session_state()
    add_shortcut()
    display_sidebar()

    display_instructions()
    evaluate_text()

    show_evaluation_buttons()
    form_field_with_placeholder("修正した文章")
    submit_feedback()

if __name__ == "__main__":
    main()
