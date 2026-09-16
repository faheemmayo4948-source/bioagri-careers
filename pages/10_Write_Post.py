import time
import streamlit as st
from lib.cloudinary_client import upload_image
from lib.firebase_client import create_blog_post

st.set_page_config(page_title="Write Post · BioAgri Careers", page_icon="✍️")

if "blog_admin_authenticated" not in st.session_state:
    st.session_state.blog_admin_authenticated = False

if not st.session_state.blog_admin_authenticated:
    st.title("🔒 Admin Access Required")
    password = st.text_input("Enter admin password", type="password")
    if st.button("Unlock"):
        if password == st.secrets.get("admin_password"):
            st.session_state.blog_admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

st.title("✍️ Write a Blog Post")

title = st.text_input("Post title*")
category = st.selectbox("Category", ["Career Advice", "Scholarships", "Internships", "Study Tips", "News", "Other"])
content = st.text_area("Content*", height=300)
uploaded_image = st.file_uploader("Cover image (optional)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Preview", use_container_width=True)

if st.button("Publish post", type="primary"):
    if not title or not content:
        st.error("Title and content are required.")
    else:
        with st.spinner("Publishing..."):
            try:
                image_url = None
                if uploaded_image:
                    file_bytes = uploaded_image.getvalue()
                    file_name = f"blog_{int(time.time())}_{uploaded_image.name}"
                    image_url = upload_image(file_bytes, file_name)

                create_blog_post(title, content, category, image_url, "BioAgri Careers Team")
                st.success("Post published!")
            except Exception as e:
                st.error(f"Failed to publish: {e}")

if st.button("🔒 Lock again"):
    st.session_state.blog_admin_authenticated = False
    st.rerun()
