import streamlit as st
import requests
import base64
from process.constants import Config
import random
import string



@st.cache_data(ttl=86400, show_spinner=False, max_entries=100)
def _generate_random_state(length=16):
    """
    Cognitoのstate値を取得
    ランダムな文字列を生成してstateパラメータとして使用する
    cache_dataとして保持しておくことでstateパラメータのチェックが可能

    Returns:
        state値
    """
    letters_and_digits = string.ascii_letters + string.digits
    random_state= ''.join(random.choice(letters_and_digits) for _ in range(length))
    return random_state

def _initialise_st_state_vars():
    """
    Cognito関連のセッション情報の初期化

    Returns:
        Nothing.
    """
    # 認可コード
    if "auth_code" not in st.session_state:
        st.session_state["auth_code"] = ""
    # Cognitoの認証チェック
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    # ユーザ情報
    if "user_info" not in st.session_state:
        st.session_state["user_info"] = ""
    # Cognitoのstateパラメータを生成してセッションに保持
    if "state" not in st.session_state:
        st.session_state['state'] = _generate_random_state()


def _get_auth_code():
    """
    ログイン後にGETでパラメータから認可コード(code)を取得

    Returns:
        auth_code: 認可コード

    """
    # experimental_get_query_params(GET)でURLからパラメータを取得
    auth_query_params = st.query_params.to_dict()
    try:
        # 認可コードをパラメータから取得
        auth_code = auth_query_params.get("code")
        # stateパラメータを取得
        received_state = auth_query_params.get("state")
        # stateパラメータがセッションに保持したものと一致しているか
        # if st.session_state['state'] != received_state:
        #     raise KeyError
    except (KeyError, TypeError):
        auth_code = ""
    return auth_code


def _set_auth_code():
    """
    認可コードをセッションに保持

    Returns:
        Nothing.
    """
    # セッションの初期化
    _initialise_st_state_vars()
    # 認証コードを取得
    auth_code = _get_auth_code()
    st.session_state["auth_code"] = auth_code


def _get_user_tokens(auth_code):
    """
    トークンURLに対しCoginitoのクライアントID、クライアントシークレット、取得した認可コードをもとに
    ユーザ認証してアクセストークンとIDトークンを取得

    Args:
        auth_code: Cognitoサーバから取得した認可コード

    Returns:
        {
        'access_token': ユーザ認証に成功した場合、cognitoサーバからアクセストークンを取得
        'id_token': ユーザ認証に成功した場合、cognitoサーバからIDトークンを取得
        }

    """

    # トークンエンドポイント
    token_url = f"{Config.COGNITO_DOMAIN}/oauth2/token"
    client_secret_string = f"{Config.CLIENT_ID}:{Config.CLIENT_SECRET}"
    client_secret_encoded = str(
        base64.b64encode(client_secret_string.encode("utf-8")), "utf-8"
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_secret_encoded}",
    }
    body = {
        "grant_type": "authorization_code",
        "client_id": Config.CLIENT_ID,
        "code": auth_code,
        "redirect_uri": Config.APP_URI,
    }
    token_response = requests.post(token_url, headers=headers, data=body)
    try:
        access_token = token_response.json()["access_token"]
        id_token = token_response.json()["id_token"]
    except (KeyError, TypeError):
        access_token = ""
        id_token = ""

    return access_token, id_token


def _get_user_info(access_token):
    """
    取得したアクセストークンでユーザ情報を取得

    Args:
        access_token: cognitoのユーザープールから取得したアクセストークン

    Returns:
        userinfo_response: json object.
    """
    # ユーザ情報エンドポイント
    userinfo_url = f"{Config.COGNITO_DOMAIN}/oauth2/userInfo"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {access_token}",
    }

    userinfo_response = requests.get(userinfo_url, headers=headers)

    return userinfo_response.json()


def set_st_state_vars():
    """
    取得した認証コード、アクセストークン、IDトークンをユーザ情報の取得、セッションへの保持
    Returns:
        Nothing.
    """
    # セッション情報の初期化
    _initialise_st_state_vars()

    # ログイン前は認可コードは取得できない。
    # ログイン後初めて認可コードをURLから取得
    auth_code = _get_auth_code()
    # アクセストークン、IDトークンを取得
    access_token, id_token = _get_user_tokens(auth_code)

    # アクセストークンを取得できたら、セッションに保持
    if access_token != "":
        st.session_state["auth_code"] = auth_code
        st.session_state["authenticated"] = True
        # カスタム属性の取得には属性の読み取りおよび書き込み許可で許可する必要あり
        st.session_state["user_info"] = _get_user_info(access_token)


def button_login():
    """
    ログインコンテンツの出力
    Returns:
        ログインコンテンツのHTML
    """
    # Authorization Code Grant（認可コード許可）
    # ログインボタンにCognitoのホストUI（ログイン画面）のリンクを設定
    login_link = f"{Config.COGNITO_DOMAIN}/login?client_id={Config.CLIENT_ID}&state={st.session_state['state']}&response_type=code&scope=openid&redirect_uri={Config.APP_URI}"
    html_button_login = f"""
        <div class='inline-block'>
            <a href='{login_link}' class='inline-block button-login' target='_self'>ログインする</a>
        </div>
    """

    return st.markdown(f"{html_button_login}", unsafe_allow_html=True)

def button_logout():
    """
    ログアウトコンテンツの出力（サイドバー）
    Returns:
        ログアウトコンテンツのHTML
    """
    logout_link = f"{Config.COGNITO_DOMAIN}/logout?client_id={Config.CLIENT_ID}&state={st.session_state['state']}&response_type=code&redirect_uri={Config.APP_URI}"
    html_button_logout = f"""
        <a href='{logout_link}' class='button-logout' target='_self'>ログアウト</a>
    """
    return st.sidebar.markdown(f"{html_button_logout}", unsafe_allow_html=True)