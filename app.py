import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
import cv2

# 设置网页背景颜色
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e0f7fa;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

st.set_page_config(page_title="美圖中心", page_icon="🖼️", initial_sidebar_state="collapsed")

st.title("美圖中心")

uploaded_file = st.file_uploader("請上傳一張圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="原始圖片", use_column_width=True)

    # 調色功能
    st.sidebar.header("調色選項")
    brightness = st.sidebar.slider("亮度", 0.0, 2.0, 1.0)
    contrast = st.sidebar.slider("對比度", 0.0, 2.0, 1.0)
    saturation = st.sidebar.slider("飽和度", 0.0, 2.0, 1.0)

    enhancer = ImageEnhance.Brightness(image)
    image_enhanced = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(image_enhanced)
    image_enhanced = enhancer.enhance(contrast)

    enhancer = ImageEnhance.Color(image_enhanced)
    image_enhanced = enhancer.enhance(saturation)

    # 去除背景功能
    st.sidebar.header("背景選項")
    remove_bg = st.sidebar.checkbox("去除背景")

    if remove_bg:
        image_np = np.array(image_enhanced)
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        mask = np.zeros(image_rgb.shape[:2], np.uint8)

        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        rect = (10, 10, image_rgb.shape[1] - 10, image_rgb.shape[0] - 10)
        cv2.grabCut(image_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image_rgb_nobg = image_rgb * mask2[:, :, np.newaxis]

        image_enhanced = Image.fromarray(image_rgb_nobg)

    st.image(image_enhanced, caption="修改後", use_column_width=True)

    # 下載處理後的圖片
    st.sidebar.header("下載處理後的圖片")
    if st.sidebar.button("下載"):
        image_enhanced.save("processed_image.png")
        with open("processed_image.png", "rb") as file:
            btn = st.sidebar.download_button(
                label="下載圖片",
                data=file,
                file_name="processed_image.png",
                mime="image/png"
            )
