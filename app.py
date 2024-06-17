import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import io
import base64

# 设置页面配置
st.set_page_config(page_title="圖片處理應用", page_icon="🖼️", initial_sidebar_state="collapsed")

# 设置网页背景颜色
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e0f7fa;
}
.image-container {
    display: inline-block;
    margin: 10px;
    text-align: left;
}
.image-container img {
    width: 300px;
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
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

st.title("圖片處理應用")

def image_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

uploaded_file = st.file_uploader("上傳一張圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # 显示原始图片和标题
    st.markdown(
        f"""
        <div class="image-container">
            <div class="image-title">原始圖片</div>
            <img src="data:image/png;base64,{image_to_base64(image)}" alt="原始圖片">
        </div>
        """, unsafe_allow_html=True
    )

    # 裁切功能
    st.sidebar.header("裁切選項")
    crop_box = st.sidebar.checkbox("裁切圖片")
    if crop_box:
        crop_width = st.sidebar.slider("裁切寬度", 0, image.width, image.width)
        crop_height = st.sidebar.slider("裁切高度", 0, image.height, image.height)
        image = image.crop((0, 0, crop_width, crop_height))

    # 調色功能
    st.sidebar.header("調色選項")
    color_mode = st.sidebar.selectbox("色調模式", ["原始", "紅色調", "藍色調", "黑白色調"])

    if color_mode == "紅色調":
        r, g, b = image.split()
        red_image = Image.merge("RGB", (r, Image.new("L", r.size, 0), Image.new("L", r.size, 0)))
        image = ImageEnhance.Color(red_image).enhance(2.0)
    elif color_mode == "藍色調":
        r, g, b = image.split()
        blue_image = Image.merge("RGB", (Image.new("L", r.size, 0), Image.new("L", r.size, 0), b))
        image = ImageEnhance.Color(blue_image).enhance(2.0)
    elif color_mode == "黑白色調":
        image = ImageOps.grayscale(image)
    
    # 分割线
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 显示修改后的图片和标题
    st.markdown(
        f"""
        <div class="image-container">
            <div class="image-title">修改後</div>
            <img src="data:image/png;base64,{image_to_base64(image)}" alt="修改後">
        </div>
        """, unsafe_allow_html=True
    )

    # 下載處理後的圖片
    st.sidebar.header("下載處理後的圖片")
    if st.sidebar.button("下載"):
        image.save("processed_image.png")
        with open("processed_image.png", "rb") as file:
            btn = st.sidebar.download_button(
                label="下載圖片",
                data=file,
                file_name="processed_image.png",
                mime="image/png"
            )
