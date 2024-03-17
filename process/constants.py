import os
import streamlit as st
class Config():
  COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN", st.secrets["COGNITO_DOMAIN"])
  CLIENT_ID = os.getenv("CLIENT_ID", st.secrets["CLIENT_ID"])
  CLIENT_SECRET = os.getenv("CLIENT_SECRET", st.secrets["CLIENT_SECRET"])
  APP_URI = os.getenv("APP_URI", st.secrets["APP_URI"])

