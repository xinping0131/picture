import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import io
import base64

# 设置页面配置
st.set_page_config(page_title="Picture Magic House!", page_icon="pic.jpg", initial_sidebar_state="collapsed")

# 设置网页背景颜色
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

#st.title("Picture Magic House!")
st.title('<img src="pic.png" width="30" height="30" style="vertical-align: middle;"> Picture Magic House!', unsafe_allow_html=True)

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

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
    st.sidebar.markdown('<span style="font-size: 40px; font-weight: bold; color: purple;">Tools</span>', unsafe_allow_html=True)
    st.sidebar.header("裁切選項")
    crop_box = st.sidebar.checkbox("裁切圖片")
    if crop_box:
        crop_left = st.sidebar.slider("左邊", 0, image.width, 0)
        crop_right = st.sidebar.slider("右邊", 0, image.width, image.width)
        crop_top = st.sidebar.slider("上方", 0, image.height, 0)
        crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height)
        image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

    # 模糊功能
    st.sidebar.header("模糊選項")
    blur_box = st.sidebar.checkbox("模糊圖片")
    if blur_box:
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
    st.sidebar.header("下載圖片")
    if st.sidebar.button("Dowload..."):
        image.save("processed_image.png")
        with open("processed_image.png", "rb") as file:
            btn = st.sidebar.download_button(
                label="下載圖片",
                data=file,
                file_name="processed_image.png",
                mime="image/png"
            )
