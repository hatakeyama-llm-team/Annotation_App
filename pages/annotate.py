import streamlit as st

from login import login_page_show
from process.auth import check_auth
from repository.cloud_sql_mysql.datasets import DataSetsRepository
from repository.cloud_sql_mysql.user_execute_count import UserExecuteRepository
from repository.cloud_sql_mysql.evaluate_status import EvaluateStatusRepository
from utils import Constants  # GOOD, PENDING, BAD などの定数を含む外部ファイル
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
        st.session_state['unprocessed_counts'] = \
        user_execute_repository.findCountByUserName(st.session_state.get('user_name'))[2]

    if 'evaluate_point' not in st.session_state:
        st.session_state['evaluate_point'] = 0
    if 'dataset_id' not in st.session_state:
        st.session_state['dataset_id'] = dataset_repository.randomChoiseIdByUnprocessed().id
    if 'dataset_text' not in st.session_state:
        st.session_state['dataset_text'] = dataset_repository.findOneById(st.session_state.get('dataset_id')).cleaned_text
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
            
            1. {Constants.VERY_GOOD}：ヘッダー、内容、フッター３つすべてをつなげた文章が意味をなしていて、良いと思える内容の場合
                
                良い内容:　誰かがお金を払ってでも読みたそうな記事(解説、小説、インタビュー、ニュース、オリジナルな文章、辞書
            
            2. {Constants.GOOD}：ヘッダー、内容、フッター３つすべてをつなげた文章が意味をなしているが、普通の内容の場合
                
                普通 : 広告など、ありきたりな内容
            
            3. {Constants.PENDING}：ヘッダー、内容、フッターのうち、1,2つ意味をなしているが、普通の内容の場合
                
                普通 :　広告など、ありきたりな内容

            4. {Constants.BAD}：ヘッダー、内容、フッターをつなげた文章が意味をなしていない場合あるいは、悪い内容の場合
                
                悪い:　公序良俗などに反する

            
            ''')

    st.markdown(f"**ヘッダー**\n\n{st.session_state.get('dataset_text')[:100]}\n\n**内容**\n"
                f"\n{st.session_state.get('dataset_text')[100:200]}\n"
                f"\n**フッター**\n\n{st.session_state.get('dataset_text')[200:300]}")

    if st.session_state.get('q1_answered') == False:
        st.warning('Q1の回答をお願いします')


def handle_evaluation(evaluation_point):
    st.session_state['evaluate_point'] = evaluation_point


def form_field_with_placeholder(label):
    with st.expander("Q2.次の文章を、意味をなす文章に修正して下さい", expanded=False):
        st.markdown(f'''
            意味をなす文章にしてください。
        ''')
    feedback_text = st.text_area(label, value=st.session_state.get('dataset_text'), key=label, height=220)
    st.session_state['feedback_text'] = feedback_text
    st.markdown('---')


def show_evaluation_buttons():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(Constants.VERY_GOOD, on_click=handle_evaluation_callback):
            evaluate_point = Constants.VERY_GOOD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col2:
        if st.button(Constants.GOOD, on_click=handle_evaluation_callback):
            evaluate_point = Constants.GOOD_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col3:
        if st.button(Constants.PENDING, on_click=handle_evaluation_callback):
            evaluate_point = Constants.PENDING_POINT
            st.session_state['q1_answered'] = True
            handle_evaluation(evaluate_point)
            st.success('↑')
    with col4:
        if st.button(Constants.BAD, on_click=handle_evaluation_callback):
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
    add_keyboard_shortcuts({'Shift+D': Constants.PENDING})
    add_keyboard_shortcuts({'Shift+F': Constants.BAD})

def change_next_dataset():
    st.session_state['user_counts'] += 1
    st.session_state['unprocessed_counts'] -= 1

    user_execute_repository = UserExecuteRepository()
    evaluate_status_repository = EvaluateStatusRepository()
    dataset_repository = DataSetsRepository()
    evaluate_status_repository.insert(st.session_state.get('dataset_id'),
                                      st.session_state.get('evaluate_point'),
                                      st.session_state.get('feedback_text'),
                                      st.session_state.get('category'),
                                      ),
    user_execute_repository.upsert(st.session_state.get('user_name'))
    st.session_state['dataset_id'] = dataset_repository.randomChoiseIdByUnprocessed().id
    st.session_state['dataset_text'] = (dataset_repository.
                                        findOneById(st.session_state.get('dataset_id')).cleaned_text)
    st.session_state['q1_answered'] = False
    st.session_state['category'] = ''


def submit_feedback():

    with st.form(key='submit_form'):
        st.form_submit_button(
            label='評価を送信する',on_click= change_next_dataset
        )
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
    st.session_state['category'] = st.radio(

        'テキストのカテゴリを選んでください',
        (
            '執筆',
            'ロールプレイ',
            'コーディング', 'テキスト抽出',
            '推論', '知識(人文学)',
            '知識(自然科学)',
            '知識(科学技術)',
            '広告',
        ),
        horizontal=True
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
