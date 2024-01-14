import streamlit as st
from webui_pages.utils import *

def register_page(api: ApiRequest,is_lite: bool = False):
    """注册页面"""
    st.write("注册页面")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    confirm_password = st.text_input("确认密码", type="password")

    if st.button("注册"):
        if password != confirm_password:
            st.error("两次输入的密码不一致，请重新输入。")
        else:
            # 在此处编写注册逻辑
            st.success("注册成功！")
            st.write("请返回登录页面进行登录。")