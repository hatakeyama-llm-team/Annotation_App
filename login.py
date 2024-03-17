import streamlit as st
import authenticate as authenticate
from pages import management, annotate

authenticate.set_st_state_vars()
authenticate.set_style_login()
if st.session_state["authenticated"]:
	authenticate.button_logout()
	try:
		annotate.show()
		user_name = st.session_state["user_info"]["name"]
		if user_name == 'admin':
			management.show()
		else:
			st.warning("管理者権限がありません")

	except Exception as e:
		st.error(f"エラーが発生しました: {e}")
else:
	st.markdown("## ログインあるいは新規登録をしてください")
	authenticate.button_login()
	# ユーザーの新規登録は未実装。とりあえずCognitoのSignInページに飛ばす
	# authenticate.button_signup()