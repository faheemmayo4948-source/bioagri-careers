import streamlit as st
import pandas as pd
from lib.firebase_client import post_job

st.set_page_config(page_title="Post a Listing · BioAgri Careers", page_icon="📝")

st.title("📝 Post a Job, Internship, or Scholarship")
st.caption("Free to post. Listings are reviewed before going live (usually within a day).")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first to post a listing.")
    st.page_link("pages/4_My_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()


@st.cache_data
def load_categories():
    return pd.read_csv("data/categories.csv")["Category"].tolist()


with st.form("post_job_form"):
    title = st.text_input("Title*", placeholder="e.g. Agriculture Extension Intern, or MS Scholarship in Plant Pathology")
    organization = st.text_input("Organization / University name*", placeholder="e.g. Green Fields Research Lab")
    category = st.selectbox("Category*", load_categories())
    job_type = st.selectbox(
        "Type*",
        ["Internship", "Full-time", "Part-time", "Research Assistantship", "Volunteer", "Scholarship"],
    )

    funding = None
    if job_type == "Scholarship":
        funding = st.text_input(
            "Funding details",
            placeholder="e.g. Fully funded, or PKR 50,000/month stipend",
        )

    location = st.text_input("Location*", placeholder="e.g. Lahore, or Remote, or Country name for scholarships")
    description = st.text_area("Description*", placeholder="Describe the role/program, eligibility, etc.")
    requirements = st.text_area("Requirements / Eligibility", placeholder="e.g. BS in Biology, minimum CGPA, IELTS score")
    deadline = st.text_input("Application deadline", placeholder="e.g. 30 October 2026")
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
                    funding=funding,
                    poster_uid=st.session_state.user["uid"],
                    poster_email=st.session_state.user["email"],
                )
                st.success("Submitted! Your listing will appear once approved.")
            except Exception as e:
                st.error(f"Failed to submit: {e}")
