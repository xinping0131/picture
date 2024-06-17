import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import io
import base64

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

# 模拟用户订阅情况
subscription_status = st.sidebar.checkbox("订阅会员")

# 如果未订阅，限制使用调整功能的次数为 10 次
if not subscription_status:
    remaining_adjustments = 10
else:
    remaining_adjustments = None  # 不限制次数

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
    
    # 图像调整功能
    st.sidebar.markdown('<span style="font-size: 35px; font-weight: bold; color: purple;">📌Tools</span>', unsafe_allow_html=True)
    st.sidebar.header("调整选项")
    
    if remaining_adjustments is not None and remaining_adjustments <= 0:
        st.sidebar.warning("您的调整次数已用尽，请订阅会员获取更多功能！")
    else:
        crop_left = st.sidebar.slider("左边", 0, image.width, 0)
        crop_right = st.sidebar.slider("右边", 0, image.width, image.width)
        crop_top = st.sidebar.slider("上方", 0, image.height, 0)
        crop_bottom = st.sidebar.slider("下方", 0, image.height, image.height)
        image = image.crop((crop_left, crop_top, crop_right, crop_bottom))

        blur_radius = st.sidebar.slider("模糊程度", 0, 10, 2)
        image = image.filter(ImageFilter.GaussianBlur(blur_radius))

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
    if st.sidebar.button("下载..."):
        image.save("processed_image.png")
        with open("processed_image.png", "rb") as file:
            btn = st.sidebar.download_button(
                label="下载图片",
                data=file,
                file_name="processed_image.png",
                mime="image/png"
            )
