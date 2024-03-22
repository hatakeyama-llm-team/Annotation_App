import streamlit as st

from login import login_page_show
from process.auth import check_auth
from repository.datasets import DataSetsRepository
from repository.user_execute_count import UserExecuteRepository
from repository.evaluate_status import EvaluateStatusRepository
from utils import Constants, v_spacer  # GOOD, PENDING, BAD などの定数を含む外部ファイル
from streamlit_shortcuts import add_keyboard_shortcuts
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
    if 'category' not in st.session_state:
        st.session_state['category'] = ''
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
    with st.expander("### Q1.次の文章を読んで評価してください(必須)", expanded=False):
        st.markdown(f'''
            【定義】
            1. **ヘッダー**：文章の冒頭部分。文章の0文字目から100文字目までの部分
            2. **内容**：文章の中心部分。文章の100文字目から200文字目までの部分
            3. **フッター**：文章の終わり部分。文章の200文字目から300文字目までの部分
            
            【評価基準】
            
            次の評価基準に従って評価してください。
            
            1. {Constants.VERY_GOOD}：ヘッダー、内容、フッター３つすべてをつなげた文章が意味をなしていて、内容も良い場合
            2. {Constants.GOOD}：ヘッダー、内容、フッター３つすべてをつなげた文章が意味をなしている場合
            3. {Constants.PENDING_1}：ヘッダー、内容、フッターのうち、２つ意味をなしている場合
            4. {Constants.PENDING_2}：ヘッダー、内容、フッターのうち、１つ意味をなしている場合
            5. {Constants.BAD}：ヘッダー、内容、フッターをつなげた文章が意味をなしていない場合
            
            ''')

    st.markdown(f"**ヘッダー**\n\n{st.session_state.get('dataset_text')[:100]}\n\n**内容**\n"
                f"\n{st.session_state.get('dataset_text')[100:200]}\n"
                f"\n**フッター**\n\n{st.session_state.get('dataset_text')[200:300]}")

    if st.session_state.get('q1_answered') == False:
        st.warning('Q1の回答をお願いします')


def handle_evaluation(evaluation_point):
    st.session_state['evaluate_point'] = evaluation_point

def form_field_with_placeholder( label ):
    with st.expander("Q2.次の文章を、意味をなす文章に修正して下さい", expanded=False):
        st.markdown(f'''
            意味をなす文章にしてください。
        ''')
    feedback_text = st.text_area(label, value=st.session_state.get('dataset_text'), key=label,height=220)
    st.session_state['feedback_text'] = feedback_text
    st.markdown('---')


def show_evaluation_buttons():
    col1,col2, col3,col4,col5 = st.columns(5)
    with col1:
        if st.button(Constants.VERY_GOOD,on_click=handle_evaluation_callback):
            evaluate_point = Constants.VERY_GOOD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col2:
        if st.button(Constants.GOOD,on_click=handle_evaluation_callback):
            evaluate_point = Constants.GOOD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col3:
        if st.button(Constants.PENDING_1,on_click=handle_evaluation_callback):
            evaluate_point = Constants.PENDING_POINT_1
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col4:
        if st.button(Constants.PENDING_2,on_click=handle_evaluation_callback):
            evaluate_point = Constants.PENDING_POINT_2
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col5:
        if st.button(Constants.BAD,on_click=handle_evaluation_callback):
            evaluate_point = Constants.BAD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    st.markdown('---')

def handle_evaluation_callback():
    st.session_state['q1_answered'] = True
def add_shortcut():
    add_keyboard_shortcuts({'Shift+A': Constants.VERY_GOOD})
    add_keyboard_shortcuts({'Shift+S': Constants.GOOD})
    add_keyboard_shortcuts({'Shift+D':Constants.PENDING_1})
    add_keyboard_shortcuts({'Shift+C':Constants.PENDING_2})
    add_keyboard_shortcuts({'Shift+E':Constants.BAD})

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
                                          st.session_state.get('category'),
                                        ),
        user_execute_repository.upsert(st.session_state.get('user_name'))
        st.session_state['dataset_id'] = dataset_repository.randomChoiseIdByUnprocessed()[0]
        st.session_state['dataset_text'] = dataset_repository.findOneById(st.session_state.get('dataset_id'))[0]
        st.session_state['q1_answered'] = False
        st.session_state['category'] = ''

        st.write('回答ありがとうございます！')
        initialize_session_state()





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

def evaluate_text_category():

    with st.expander("Q3.文章のカテゴリを選んでください(任意）", expanded=False):
        st.markdown(Constants.CATEGORY_INSTRUCTIONS)
    st.session_state['category'] = st.selectbox(
        'テキストのカテゴリを選んでください',
        ('','広告', 'コーディング', 'テキスト抽出', '数学','ロールプレイ',
         'STEM', 'ライティング技術', '人文学', '歴史', '哲学', '文学',
         '芸術', '言語学', '文化人類学', '社会学', '宗教学', '倫理学'
         ),
        placeholder='',
    )
    st.markdown('---')

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
    evaluate_text_category()
    submit_feedback()

if __name__ == "__main__":
    main()
