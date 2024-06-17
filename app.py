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

# 會員訂閱價格
subscription_price = 3  # 美元每月

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def login():
    st.subheader("登入")
    username = st.text_input("帳戶名稱")
    password = st.text_input("密碼", type="password")
    if st.button("登入"):
        if username in user_db and user_db[username] == password:
            st.success(f"歡迎回來，{username}！")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("帳戶名稱或密碼不正確！")

def logout():
    st.subheader("登出")
    if st.button("登出"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.info("您已成功登出！")

def register():
    st.subheader("註冊新帳號")
    username = st.text_input("請輸入帳戶名稱")
    password = st.text_input("請輸入密碼", type="password")
    if st.button("註冊"):
        if username in user_db:
            st.error("帳戶名稱已存在，請選擇其他名稱！")
        else:
            user_db[username] = password
            st.success("註冊成功！請進行登入。")

def subscription():
    st.sidebar.subheader("會員訂閱")
    option = st.sidebar.selectbox("是否訂閱會員", ["未訂閱", "訂閱"])
    if option == "未訂閱":
        remaining_trials = st.session_state.get("remaining_trials", 3)
        if remaining_trials <= 0:
            st.warning("您已使用完免費次數，請考慮訂閱以繼續使用功能。")
        else:
            st.info(f"您還有 {remaining_trials} 次免費使用機會。")
            st.session_state.remaining_trials = remaining_trials - 1
    else:  # 訂閱會員
        st.info("訂閱後可無限次使用圖片調整功能。")

def main():
    st.set_page_config(page_title="Picture Magic House!", page_icon="✨", initial_sidebar_state="collapsed")
    st.markdown(
        """
        <style>
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
        </style>
        """, unsafe_allow_html=True
    )

    st.title("Picture Magic House!🎩")
    
    if not st.session_state.get("logged_in", False):
        st.warning("請先登入或註冊！")
        option = st.radio("選擇註冊或登入", ["註冊", "登入"])
        if option == "註冊":
            register()
        else:
            login()
    else:
        subscription()
        uploaded_file = st.file_uploader("請上傳一張圖片^^", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            # 顯示原始圖片和標題
            st.markdown(
                f"""
                <div class="image-container">
                    <div class="image-title">原始圖片🖼️</div>
                    <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始圖片🖼️">
                </div>
                """, unsafe_allow_html=True
            )

            # 左側欄顯示圖片調整功能
            st.sidebar.markdown('<span style="font-size: 20px; font-weight: bold;">圖片調整功能</span>', unsafe_allow_html=True)

            # 裁切功能
            st.sidebar.subheader("裁切選項")
            crop_left = st.sidebar.slider("左邊", 0, image.width, 0)
            crop_right = st.sidebar.slider("右邊", 0, image.width, image.width)
            crop_top = st.sidebar.slider("上方", 0, image.height, 0)
            crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height)
            image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

            # 模糊功能
            st.sidebar.subheader("模糊選項")
            blur_radius = st.sidebar.slider("模糊程度", 0, 10, 2)
            image = image.filter(ImageFilter.GaussianBlur(blur_radius))

            # 調整功能
            st.sidebar.subheader("調整選項")
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
          
            # 顯示修改後的圖片和標題
            st.markdown(
                f"""
                <div class="image-container">
                    <div class="image-title">修改後~</div>
                    <img src="data:image/png;base64,{image_to_base64(image)}" alt="修改後~">
                </div>
                """, unsafe_allow_html=True
            )

            # 下載處理後的圖片
            st.sidebar.subheader("下載圖片")
            if st.sidebar.button("下載圖片"):
                image.save("processed_image.png")
                with open("processed_image.png", "rb") as file:
                    btn = st.sidebar.download_button(
                        label="下載圖片",
                        data=file,
                        file_name="processed_image.png",
                        mime="image/png"
                    )

            # 登出功能
            logout()

if __name__ == "__main__":
    main()
