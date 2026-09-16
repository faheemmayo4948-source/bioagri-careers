import streamlit as st
import pandas as pd
from lib.firebase_client import post_job

st.set_page_config(page_title="Post a Job · BioAgri Careers", page_icon="📝")

st.title("📝 Post a Job or Internship")
st.caption("Free to post. Listings are reviewed before going live (usually within a day).")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first to post a listing.")
    st.page_link("pages/4_My_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()


@st.cache_data
def load_categories():
    return pd.read_csv("data/categories.csv")["Category"].tolist()


with st.form("post_job_form"):
    title = st.text_input("Job/Internship title*", placeholder="e.g. Agriculture Extension Intern")
    organization = st.text_input("Organization name*", placeholder="e.g. Green Fields Research Lab")
    category = st.selectbox("Category*", load_categories())
    job_type = st.selectbox("Type*", ["Internship", "Full-time", "Part-time", "Research Assistantship", "Volunteer"])
    location = st.text_input("Location*", placeholder="e.g. Lahore, or Remote")
    description = st.text_area("Description*", placeholder="Describe the role, responsibilities, etc.")
    requirements = st.text_area("Requirements", placeholder="e.g. BS in Biology, familiarity with lab techniques")
    deadline = st.text_input("Application deadline (optional)", placeholder="e.g. 30 October 2026")
    contact = st.text_input("Contact email or application link*", placeholder="e.g. jobs@company.com or https://...")

    submitted = st.form_submit_button("Submit for review", type="primary")

    if submitted:
        if not all([title, organization, location, description, contact]):
            st.error("Please fill all required fields (marked with *).")
        else:
            try:
                post_job(
                    title, organization, category, job_type, location,
                    description, requirements, deadline, contact,
                    poster_uid=st.session_state.user["uid"],
                    poster_email=st.session_state.user["email"],
                )
                st.success("Submitted! Your listing will appear once approved.")
            except Exception as e:
                st.error(f"Failed to submit: {e}")
