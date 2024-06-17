import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io
import base64

# 模擬帳戶資料庫
user_db = {}

def register():
    with st.form(key="registration_form"):
        username = st.text_input("請輸入帳戶名稱")
        password = st.text_input("請輸入密碼", type="password")
        submit_button = st.form_submit_button("註冊")

        if submit_button:
            if username in user_db:
                st.error("帳戶名稱已存在，請選擇其他名稱！")
            else:
                user_db[username] = password
                st.success("註冊成功！")
                st.session_state.logged_in = True
                st.session_state.username = username

def login():
    with st.form(key="login_form"):
        username = st.text_input("帳戶名稱")
        password = st.text_input("密碼", type="password")
        submit_button = st.form_submit_button("登入")

        if submit_button:
            if username in user_db and user_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("登入成功！")
            else:
                st.error("帳戶名稱或密碼不正確！")

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def main():
    if st.session_state.logged_in:
        st.title("Picture Magic House!🎩")
        uploaded_file = st.file_uploader("請上傳一張圖片^^", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            # 显示原始图片和标题
            st.markdown(
                f"""
                <div class="image-container">
                    <div class="image-title">原始圖片🖼️</div>
                    <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始圖片🖼️">
                </div>
                """, unsafe_allow_html=True
            )
            
            # 裁切功能
            st.sidebar.markdown('<span style="font-size: 35px; font-weight: bold; color: purple;">📌Tools</span>', unsafe_allow_html=True)
            st.sidebar.header("裁切選項")
            
            crop_left = st.sidebar.slider("左邊", 0, image.width, 0)
            crop_right = st.sidebar.slider("右邊", 0, image.width, image.width)
            crop_top = st.sidebar.slider("上方", 0, image.height, 0)
            crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height)
            image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

            # 模糊功能
            st.sidebar.header("模糊選項")
            blur_radius = st.sidebar.slider("模糊程度", 0, 10, 2)
            image = image.filter(ImageFilter.GaussianBlur(blur_radius))

            # 調整功能
            st.sidebar.header("調整選項")
            color_mode = st.sidebar.selectbox("色調模式", ["原始", "紅色調", "藍色調", "黑白色調"])
            brightness = st.sidebar.slider("亮度", 0.0, 2.0, 1.0)
            contrast = st.sidebar.slider("對比度", 0.0, 2.0, 1.0)
            saturation = st.sidebar.slider("飽和度", 0.0, 2.0, 1.0)

            if color_mode == "紅色調":
                r, g, b = image.split()
                red_image = Image.merge("RGB", (r, Image.new("L", r.size, 0), Image.new("L", r.size, 0)))
                enhancer = ImageEnhance.Color(red_image)
                image = enhancer.enhance(saturation)
            elif color_mode == "藍色調":
                r, g, b = image.split()
                blue_image = Image.merge("RGB", (Image.new("L", r.size, 0), Image.new("L", r.size, 0), b))
                enhancer = ImageEnhance.Color(blue_image)
                image = enhancer.enhance(saturation)
            elif color_mode == "黑白色調":
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
                    <div class="image-title">修改後~</div>
                    <img src="data:image/png;base64,{image_to_base64(image)}" alt="修改後~">
                </div>
                """, unsafe_allow_html=True
            )

            # 下載處理後的圖片
            st.sidebar.header("圖片處理")
            if st.sidebar.button("Download..."):
                image.save("processed_image.png")
                with open("processed_image.png", "rb") as file:
                    btn = st.sidebar.download_button(
                        label="下載圖片",
                        data=file,
                        file_name="processed_image.png",
                        mime="image/png"
                    )
            
            # 登出按鈕
            st.sidebar.header("登出")
            if st.sidebar.button("登出"):
                st.session_state.logged_in = False
                st.session_state.username = None

    else:
        st.title("歡迎來到 Picture Magic House!")
        option = st.radio("選擇註冊或登入", ["註冊", "登入"])

        if option == "註冊":
            st.header("註冊新帳號")
            register()
        else:
            st.header("登入")
            login()

# 主要應用程式入口
def app():
    # 初始化會話狀態
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    main()

if __name__ == "__main__":
    app()
