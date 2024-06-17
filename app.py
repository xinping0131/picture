import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io
import base64

# 模拟帐户数据库
user_db = {
    "user1": {"password": "password1", "subscribed": False}
}

# 设置页面配置
st.set_page_config(page_title="Picture Magic House!", page_icon="✨", initial_sidebar_state="collapsed")

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
    
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

.sidebar-section {
    margin-top: 30px;
}

</style>
"""

st.markdown(page_bg_css, unsafe_allow_html=True)

# 登录功能
def login():
    st.title("登入")
    username = st.text_input("帐户名")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        if username in user_db and user_db[username]["password"] == password:
            st.success("登录成功！")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("帐户名或密码不正确！")

# 登出功能
def logout():
    st.title("登出")
    if st.button("登出"):
        st.session_state.logged_in = False
        st.success("您已成功登出！")

# 会员订阅功能
def subscription():
    st.title("会员订阅")
    username = st.session_state.username

    if username in user_db:
        subscribed = user_db[username]["subscribed"]
        if not subscribed:
            st.write("当前未订阅")
            if st.button("订阅（每月$3）"):
                # 在此添加真实订阅逻辑，这里只是模拟
                user_db[username]["subscribed"] = True
                st.success("订阅成功！")
        else:
            st.write("当前已订阅")
    else:
        st.error("用户不存在")

# 刷卡按钮（模拟支付）
def payment():
    st.title("刷卡")
    if st.button("刷卡（$3）"):
        st.success("支付成功！")

# 主程序
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
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

            # 图片调整功能（显示在左侧）
            st.sidebar.title("图片调整选项")
            
            # 裁切功能
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

            # 下载处理后的图片
            st.sidebar.header("下载图片")
            if st.sidebar.button("Download..."):
                image.save("processed_image.png")
                with open("processed_image.png", "rb") as file:
                    btn = st.sidebar.download_button(
                        label="下载图片",
                        data=file,
                        file_name="processed_image.png",
                        mime="image/png"
                    )
            
            # 显示会员订阅信息
            st.sidebar.markdown("---")
            st.sidebar.title("会员订阅")
            if st.sidebar.button("订阅信息"):
                subscription()

            # 显示刷卡按钮
            st.sidebar.markdown("---")
            st.sidebar.title("刷卡")
            if st.sidebar.button("刷卡（$3）"):
                payment()

        else:
            st.write("请上传一张图片以开始处理。")

        # 显示登出按钮
        st.sidebar.markdown("---")
        st.sidebar.title("登出")
        if st.sidebar.button("登出"):
            st.session_state.logged_in = False
            st.success("您已成功登出！")

    else:
        login()

if __name__ == "__main__":
    main()
