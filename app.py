import streamlit as st
import os
from utils.font_utils import list_fonts, get_font_path
from utils.poster_generator import generate_poster
from utils.scraper import download_unsplash_images_api
from utils.image_generator import generate_image_from_prompt
from PIL import Image

st.set_page_config(layout="wide")
st.title("🖼 Manual Quote Poster Generator")

tab1, tab2 = st.tabs(["🌐 Scrape Backgrounds", "🖋️ Create Poster"])

with tab1:
    st.subheader("Scrape Unsplash Images")
    query = st.text_input("Search keyword", value="nature")
    count = st.slider("Number of images", 1, 10, 5)
    if st.button("Scrape Images"):
        msg = download_unsplash_images_api(query, count)
        st.success(msg)

    scraped_images = [f for f in os.listdir("images") if query in f and f.endswith(('.jpg', '.png'))]
    for img in scraped_images:
        st.image(os.path.join("images", img), width=300)

with tab2:
    st.subheader("Design Your Quote Poster")
    images = [f for f in os.listdir("images") if f.lower().endswith((".jpg", ".png"))]
    selected_img = st.selectbox("Select background image", images) if images else None

    if selected_img:
        image_path = os.path.join("images", selected_img)
        quote = st.text_area("Enter your quote or message:")

        font_list = list_fonts()
        if font_list:
            font_name = st.selectbox("Choose a font", font_list)
            font_path = get_font_path(font_name)
        else:
            st.warning("⚠️ No fonts found in the fonts directory.")
            font_path = None

        font_size = st.slider("Font size", 10, 150, 40)
        font_color = st.color_picker("Font color", "#FFFFFF")
        alignment = st.radio("Text alignment", ["left", "center", "right"])
        orientation = st.radio("Text orientation", ["horizontal", "vertical"])

        use_prompt_image = st.checkbox("🎨 Generate foreground image from prompt")
        if use_prompt_image:
            fg_prompt = st.text_input("Describe the image to overlay:")

        if st.button("Generate Poster") and font_path:
            bg_img = Image.open(image_path).convert("RGBA")
            if use_prompt_image and fg_prompt:
                fg_img = generate_image_from_prompt(fg_prompt)
                fg_img = fg_img.resize((int(bg_img.width / 2), int(bg_img.height / 2)))
                bg_img.paste(fg_img, (int(bg_img.width / 4), int(bg_img.height / 4)), fg_img.convert("RGBA"))

            final_img = generate_poster(bg_img, quote, font_path, font_size, font_color, alignment, orientation)
            st.image(final_img, use_container_width=True)
            final_img.save("generated_poster.png")
            with open("generated_poster.png", "rb") as f:
                st.download_button("Download Poster", f, file_name="quote_poster.png")
    else:
        st.info("No background image available. Please scrape images first.")