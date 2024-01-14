import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.dialogue.dialogue import dialogue_page, chat_box
from webui_pages.login.login import login_page
from webui_pages.register.register import register_page
from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
import os
import sys
from configs import VERSION
from server.utils import api_address

import streamlit_authenticator as stauth
import time

import yaml
from yaml.loader import SafeLoader

# 认证


api = ApiRequest(base_url=api_address())

if __name__ == "__main__":


    is_lite = "lite" in sys.argv

    st.set_page_config(
        "SAB WebUI",
        os.path.join("img", "chatchat_icon_blue_square_v2.png"),
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat',
            'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            'About': f"""欢迎使用 Langchain-Chatchat WebUI {VERSION}！"""
        }
    )

    pages = {
        "对话": {
            "icon": "chat",
            "func": dialogue_page,
        },
        "知识库管理": {
            "icon": "hdd-stack",
            "func": knowledge_base_page,
        },
    }

    # selected_page = "登录"  # 设置登录页面为默认选项
    #
    # if selected_page in pages:
    #     pages[selected_page]["func"](api=api, is_lite=is_lite)

    # time.sleep(5000)
    with st.sidebar:
        st.image(
            os.path.join(
                "img",
                "logo-long-chatchat-trans-v2.png"
            ),
            use_column_width=True
        )
        st.caption(
            f"""<p align="right">当前版本：{VERSION}</p>""",
            unsafe_allow_html=True,
        )
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )


    if selected_page in pages:
        if selected_page=="对话":
            pages[selected_page]["func"](api=api, is_lite=is_lite)
        elif selected_page=="知识库管理":
            with open(r'/mnt/Langchain-Chatchat/config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)
                hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
                authenticator = stauth.Authenticate(
                    config['credentials'],
                    config['cookie']['name'],
                    config['cookie']['key'],
                    config['cookie']['expiry_days'],
                    config['preauthorized'],
                )

            if authenticator.register_user('Register user', preauthorization=False):
                with open(r'/mnt/Langchain-Chatchat/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('用户注册成功')
            if authenticator.login('登录', 'main'):
                if st.session_state["authentication_status"] is True:
                    authenticator.logout('Logout', 'main', key='unique_key')
                    st.write(f'欢迎 *{st.session_state["name"]}*')
                    pages["知识库管理"]["func"](api=api, is_lite=is_lite)
                elif st.session_state["authentication_status"] is False:
                    st.error('用户名或密码错误')
                elif st.session_state["authentication_status"] is None:
                    st.warning('请输入用户名和密码')
                else:
                    st.warning("bug")









