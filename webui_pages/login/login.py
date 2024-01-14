import streamlit as st
from webui_pages.utils import *
from webui_pages.dialogue.dialogue import dialogue_page
from webui_pages.register.register import register_page
# from webui import api

# api = ApiRequest()
def login_page(api: ApiRequest, is_lite: bool = False):
    """模拟登录"""
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        if username == "admin" and password == "123":
            st.success("登录成功！")
            st.empty()
            dialogue_page(api)

        else:
            st.error("用户名或密码错误。")
            st.write("未注册？请先注册：")
            if st.button("注册"):
                register_page(api)


