import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import io
import base64

# 模拟用户数据库
user_db = {"user": "password"}  # 预设一个用户名和密码
session_limit = 3  # 非订阅用户的使用限制次数

# 设置页面配置
st.set_page_config(page_title="Picture Magic House!", page_icon="✨", initial_sidebar_state="collapsed")

# 设置网页背景颜色
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e0f7fa; /* 设置背景颜色 */
    padding: 20px; /* 页面内边距 */
}

.image-container {
    display: inline-block;
    margin: 18px;
    text-align: left;
}

.image-container img {
    max-width: 400px;
    height: auto;
}

.image-title {
    font-weight: bold;
}

.divider {
    width: 100%;
    border-top: 2px solid #bbb;
    margin: 20px 0;
}

.divider-text {
    text-align: center; /* 文字置中 */
    background-color: #ffffff; /* 文字背景色 */
    padding: 0 10px; /* 文字的左右内边距 */
    font-weight: bold; /* 字体加粗 */
    font-size: 20px; /* 字体大小 */
    margin-top: -18px; /* 调整文字位置 */
}
</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def login():
    with st.form(key="login_form"):
        username = st.text_input("账号名称")
        password = st.text_input("密码", type="password")
        submit_button = st.form_submit_button("登录")

        if submit_button:
            if username in user_db and user_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.usage_count = 0
                st.success("登录成功！")
            else:
                st.error("账号名称或密码不正确！")

def main():
    st.sidebar.title("用户区域")
    if st.session_state.logged_in:
        st.sidebar.write(f"欢迎, {st.session_state.username}!")

        subscription_status = st.sidebar.selectbox(
            "请选择订阅状态",
            ["未订阅", "订阅"]
        )

        if subscription_status == "订阅":
            st.sidebar.write("订阅用户可无限次使用图片调整功能。")
            st.session_state.subscribed = True
        else:
            st.sidebar.write(f"非订阅用户只能使用 {session_limit} 次图片调整功能。")
            st.session_state.subscribed = False

        if st.sidebar.button("登出"):
            st.session_state.logged_in = False
            st.experimental_rerun()

        if st.session_state.subscribed or st.session_state.usage_count < session_limit:
            st.title("Picture Magic House!🎩")
            uploaded_file = st.file_uploader("请上传一张图片^^", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                
                # 显示原始图片和标题
                st.markdown(
                    f"""
                    <div class="image-container">
                        <div class="image-title">原始图片🖼️</div>
                        <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始图片🖼️">
                    </div>
                    """, unsafe_allow_html=True
                )
                
                # 裁切功能
                st.sidebar.markdown('<span style="font-size: 35px; font-weight: bold; color: purple;">📌Tools</span>', unsafe_allow_html=True)
                st.sidebar.header("裁切选项")
                
                crop_left = st.sidebar.slider("左边", 0, image.width, 0)
                crop_right = st.sidebar.slider("右边", 0, image.width, image.width)
                crop_top = st.sidebar.slider("上方", 0, image.height, 0)
                crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height)
                image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

                # 模糊功能
                st.sidebar.header("模糊选项")
                blur_radius = st.sidebar.slider("模糊程度", 0, 10, 2)
                image = image.filter(ImageFilter.GaussianBlur(blur_radius))

                # 调整功能
                st.sidebar.header("调整选项")
                color_mode = st.sidebar.selectbox("色调模式", ["原始", "红色调", "蓝色调", "黑白色调"])
                brightness = st.sidebar.slider("亮度", 0.0, 2.0, 1.0)
                contrast = st.sidebar.slider("对比度", 0.0, 2.0, 1.0)
                saturation = st.sidebar.slider("饱和度", 0.0, 2.0, 1.0)

                if color_mode == "红色调":
                    r, g, b = image.split()
                    red_image = Image.merge("RGB", (r, Image.new("L", r.size, 0), Image.new("L", r.size, 0)))
                    enhancer = ImageEnhance.Color(red_image)
                    image = enhancer.enhance(saturation)
                elif color_mode == "蓝色调":
                    r, g, b = image.split()
                    blue_image = Image.merge("RGB", (Image.new("L", r.size, 0), Image.new("L", r.size, 0), b))
                    enhancer = ImageEnhance.Color(blue_image)
                    image = enhancer.enhance(saturation)
                elif color_mode == "黑白色调":
                    image = ImageOps.grayscale(image)

                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(brightness)

                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(contrast)
                
                # 分割线
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
              
                # 显示修改后的图片和标题
                st.markdown(
                    f"""
                    <div class="image-container">
                        <div class="image-title">修改后~</div>
                        <img src="data:image/png;base64,{image_to_base64(image)}" alt="修改后~">
                    </div>
                    """, unsafe_allow_html=True
                )

                # 计数调整次数
                if not st.session_state.subscribed:
                    st.session_state.usage_count += 1

                # 下载处理后的图片
                st.sidebar.header("下载图片")
                if st.sidebar.button("下载"):
                    image.save("processed_image.png")
                    with open("processed_image.png", "rb") as file:
                        btn = st.sidebar.download_button(
                            label="下载图片",
                            data=file,
                            file_name="processed_image.png",
                            mime="image/png"
                        )
        else:
            st.error("您已达到非订阅用户的使用限制次数，请订阅以继续使用。")
    else:
        st.title("欢迎来到 Picture Magic House!")
        login()

def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.subscribed = False

    main()

if __name__ == "__main__":
    app()
