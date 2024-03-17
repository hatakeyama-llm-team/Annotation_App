import random
import streamlit as st

from process.auth import check_auth
from repository.datasets import DataSetsRepository
from repository.evaluate_status import EvaluateStatusRepository
from streamlit_shortcuts import add_keyboard_shortcuts

from repository.user_execute_count import UserExecuteRepository


def show():
    GOOD = "文章が成立している😁"
    PENDING = "判断に困る🙄"
    BAD = "文章が成立していない😇"
    #
    GOOD_POINT = 100
    PENDING_POINT = 50
    BAD_POINT = 0
    # Set up the page layout
    dataset_repository = DataSetsRepository()
    user_execute_repository = UserExecuteRepository()
    evaluate_status_repository = EvaluateStatusRepository()
    try:
        dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]
    except:
        st.success("🎉全てのデータセットを評価しました！")
        st.stop()
    dataset_id = dataset_repository.randomChoiseIdByUnprocessed()[0]

    user_name = ""

    if 'user_info' in st.session_state:
        if st.session_state["user_info"] is not None:
            user_name = st.session_state["user_info"]["name"]

            st.title(f'{user_name}さん、こんにちは！')
        else:
            st.write(f'こんにちは！')
    fetched_user_processed_counts, fetched_all_counts, fetched_unprocessed_count = user_execute_repository.findCountByUserName(
            user_name)

    if fetched_user_processed_counts is None:
        fetched_user_processed_counts = 0
    if fetched_all_counts is None:
        fetched_all_counts = 0
    if fetched_unprocessed_count is None:
        fetched_unprocessed_count = 0

    user_count = st.session_state.setdefault('user_counts', fetched_user_processed_counts)
    all_count = st.session_state.setdefault('all_counts', fetched_all_counts)
    unprocessed_count = st.session_state.setdefault('unprocessed_counts', fetched_unprocessed_count)
    # Add a title to the page
    st.title("Annotation App")
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
    with st.expander("評価数の確認", expanded=True):
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
        st.markdown(f"""
        # ヘッダー
                
         {dataset_text[0][:100]}
        
        # 内容
        
        {dataset_text[0][101:200]}
        
        
        # フッター
        
        {dataset_text[0][201:300]}
        
        """)
    with st.expander("内容を読んで日本語として文章が成り立っていますか？"):
        st.markdown("""
        この文章を読んで、日本語として文章が成り立っているかどうかを評価してください。
        
        - 支離滅裂な文章や、意味が通じない文章は「文章が成立していない」に評価してください。
        
        - 日本語として文章が成り立っている場合は「文章が成立している」に評価してください。
        
        - また、判断に困る場合は「判断に困る」に評価してください。
                    """)

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



    with col1:

        if st.button(GOOD, ):
            st.success("ありがとうございます!")
            if user_name is not None:
                user_execute_repository.upsert(user_name)
                user_count += 1
                unprocessed_count -= 1

    with col2:

        if st.button(PENDING,
                     ):
            st.success("悩みますよね..!")
            if user_name is not None:
                user_execute_repository.upsert(user_name)
                user_count += 1
                unprocessed_count -= 1
    with col3:

        if st.button(BAD):
            st.success("ありがとうございます！")
            if user_name is not None:
                user_count += 1
                unprocessed_count -= 1

        with st.expander("便利なショートカットキー"):
            st.markdown(f"""

                        - {GOOD}   : Shift+A
                        - {PENDING}: Shift+S
                        - {BAD}    : Shift+D

                        """)
    with st.expander("データセットの評価数の確認"):
        st.markdown(f"""

     - **コーディングに関するデータ**：特定のプログラミング言語 　**(Python, C++, HTML/CSS)**　に関するサンプルコード、解説、およびアルゴリズムやデータ構造の解説を含むデータ。

     - **テキスト抽出と解析に関するデータ**：異なる形式のテキスト（例：映画レビュー、記事、ニュース記事）からの情報抽出に関する例や解説。

     特定の情報（例：評価、固有名詞、数値情報）の抽出方法に関するデータも有効。

     - **数学問題に関するデータ**：数学の問題とその解法を説明するテキストデータ。

     幅広いトピック（例：代数、幾何、確率論、微積分）をカバーし、問題解決のステップや考え方を詳細に説明する内容。

     - **論理的推論と問題解決に関するデータ**：論理パズル、推論問題、思考実験に関する問題と解答例。異なる種類の推論（演繹的、帰納的、類推的）に関するデータも有効。

     - **ロールプレイや想像力を駆使したシナリオに関するデータ**：創作物、対話、仮想的なシナリオにおけるキャラクターの言動や行動を示すテキストデータ。

     異なるキャラクターの視点や性格を反映した書き方に関する例も有用。

     - **STEM（科学、技術、工学、数学）に関するデータ**：科学的概念、技術的詳細、工学的問題解決方法、数学的定理や証明に関する解説。

     現実世界の応用例を含むデータで、専門用語とその解説も含める。

     - **ライティング技術に関するデータ**：文章や物語の書き方、編集と改善の方法、異なるスタイルやトーンの書き分け方に関するテキストデータ。特定のジャンルや形式（例：小説、詩、記事、メール）に特化した書き方の指南も含める。

     - **人文学**
     1. **歴史**: 世界史や日本史を含む幅広い時代と地域に関する詳細な情報。特定の出来事、文化、政治的変遷、経済的発展、社会的動向などに関するデータ。
     2. **哲学**: 西洋哲学、東洋哲学、現代哲学など、異なる哲学的思想や理論、重要な哲学者とその主張に関する詳細な説明。
     3. **文学**: 世界文学と日本文学の両方から、主要な作品、著者、文学的テーマ、文体、ジャンルに関する情報。詩、小説、劇など、様々な形式の作品についての解析や評価。
     4. **芸術**: 絵画、彫刻、建築、音楽、舞台芸術など、多岐にわたる芸術分野に関する歴史、理論、批評。重要な作品やアーティスト、芸術運動に関するデータ。
     5. **言語学**: 言語の構造、発達、使用に関する理論や研究。異なる言語の比較、方言、言語変化の原因と効果、言語学的分析手法に関する情報。
     6. **文化人類学と社会学**: 文化、信仰、習慣、社会構造、人間行動の研究。異文化間の相互作用、社会的問題、現代社会のトレンドに関する分析。
     7. **宗教学**: 世界の主要な宗教、宗教的慣習、神話、宗教的な儀式とその社会的、文化的意義に関するデータ。
     8. **倫理学**: 倫理的な問題、道徳哲学、応用倫理学（ビジネス倫理、環境倫理など）に関する理論や議論。
             """)
    evaluated_text_category = st.radio("カテゴリの分類", ("コーディング","STEM","ライティング技術",'人文学'), horizontal=True)

    if st.button("評価する"):
        evaluate_status_repository.insert(dataset_id, GOOD_POINT, evaluated_text_category)


    st.session_state['user_counts'] = user_count
    st.session_state['all_counts'] = all_count
    st.session_state['unprocessed_counts'] = unprocessed_count
    if unprocessed_count == 0:
        st.warning("全てのデータセットを評価しました！")

if __name__ == "__main__":

    if check_auth():
        show()
    else:
        st.warning("ログインしてください")
