import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io
import base64

# 模擬用戶資料庫
user_db = {"app": "123"}  # 預設一個用戶名和密碼
session_limit = 3  # 非訂閱用戶的使用限制次數

# 設置頁面配置
st.set_page_config(page_title="Picture Magic House!", page_icon="✨", initial_sidebar_state="collapsed")

# 設置網頁背景顏色
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e0f7fa; /* 設置背景顏色 */
    padding: 20px; /* 頁面內邊距 */
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
    padding: 0 10px; /* 文字的左右內邊距 */
    font-weight: bold; /* 字體加粗 */
    font-size: 20px; /* 字體大小 */
    margin-top: -18px; /* 調整文字位置 */
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
        username = st.text_input("帳號名稱")
        password = st.text_input("密碼", type="password")
        submit_button = st.form_submit_button("登入")

        if submit_button:
            if username in user_db and user_db[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.usage_count = 0
                st.success("登入成功！")
            else:
                st.error("帳號名稱或密碼不正確！")

def main():
    st.sidebar.title("用戶狀態")
    if st.session_state.logged_in:
        st.sidebar.write(f"歡迎, {st.session_state.username}~")

        subscription_status = st.sidebar.selectbox(
            "訂閱狀況",
            ["未訂閱", "訂閱(每月3 USD)"],
            key="subscription_status"
        )

        if subscription_status == "訂閱(每月3 USD)":
            st.sidebar.write("訂閱用戶可無限次使用本系統~")
            st.session_state.subscribed = True
        else:
            st.sidebar.write(f"非訂閱用戶只能上傳 {session_limit} 次圖片進行使用喔。")
            st.session_state.subscribed = False

        if st.session_state.subscribed or st.session_state.usage_count < session_limit:
            st.title("Picture Magic House!🎩")
            uploaded_file = st.file_uploader("請上傳一張圖片^^", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                st.session_state.usage_count += 1
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
                
                # 裁切功能
                st.sidebar.markdown('<span style="font-size: 35px; font-weight: bold; color: purple;">📌工具</span>', unsafe_allow_html=True)
                st.sidebar.header("裁切功能")
                
                crop_left = st.sidebar.slider("左邊", 0, image.width, 0, key="crop_left")
                crop_right = st.sidebar.slider("右邊", 0, image.width, image.width, key="crop_right")
                crop_top = st.sidebar.slider("上方", 0, image.height, 0, key="crop_top")
                crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height, key="crop_bottom")
                image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

                # 模糊功能
                st.sidebar.header("模糊功能")
                blur_radius = st.sidebar.slider("模糊程度", 0, 10, 2, key="blur_radius")
                image = image.filter(ImageFilter.GaussianBlur(blur_radius))

                # 調整功能
                st.sidebar.header("調整功能")
                color_mode = st.sidebar.selectbox("色調模式", ["原始", "紅色調", "藍色調", "黑白色調"], key="color_mode")
                brightness = st.sidebar.slider("亮度", 0.0, 2.0, 1.0, key="brightness")
                contrast = st.sidebar.slider("對比度", 0.0, 2.0, 1.0, key="contrast")
                saturation = st.sidebar.slider("飽和度", 0.0, 2.0, 1.0, key="saturation")

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
                
                # 分割線
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
              st.sidebar.header("下載圖片")
                img_buffer = io.BytesIO()
                image.save(img_buffer, format="PNG")
                img_buffer.seek(0)
                st.sidebar.download_button(
                    label="Download...",
                    data=img_buffer,
                    file_name="processed_image.png",
                    mime="image/png"
                )
                        
            else:
                if not st.session_state.subscribed and st.session_state.usage_count >= session_limit:
                    st.error("您已達到非訂閱用戶的使用限制次數，請訂閱以繼續使用，謝謝。")
        else:
            if not st.session_state.subscribed and st.session_state.usage_count >= session_limit:
                st.error("您已達到非訂閱用戶的使用限制次數，請訂閱以繼續使用，謝謝。")
    else:
        st.title("Welcome To Picture Magic House!")
        login()

    # 登出按鈕
    st.sidebar.markdown('<div style="position: fixed; bottom: 10px; width: 100%;">', unsafe_allow_html=True)
    if st.sidebar.button("登出", key="logout_button_bottom"):
        st.session_state.logged_in = False
        st.experimental_rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.subscribed = False

    main()

if __name__ == "__main__":
    app()
