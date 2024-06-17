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

                # 自動登入
                st.title("Picture Magic House!🎩")
                uploaded_file = st.file_uploader("請上傳一張圖片^^", type=["jpg", "jpeg", "png"])
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    
                    # 以下為圖片處理的代碼，這裡可以根據需要進行圖片處理操作

                    # 显示原始图片和标题
                    st.markdown(
                        f"""
                        <div class="image-container">
                            <div class="image-title">原始圖片🖼️</div>
                            <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始圖片🖼️">
                        </div>
                        """, unsafe_allow_html=True
                    )

# 其餘部分保持不變

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
            
            # 以下為圖片處理的代碼，這裡可以根據需要進行圖片處理操作

            # 显示原始图片和标题
            st.markdown(
                f"""
                <div class="image-container">
                    <div class="image-title">原始圖片🖼️</div>
                    <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始圖片🖼️">
                </div>
                """, unsafe_allow_html=True
            )

# 其餘部分保持不變

# 主要應用程式入口
def app():
    # 初始化會話狀態
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    main()

if __name__ == "__main__":
    app()
