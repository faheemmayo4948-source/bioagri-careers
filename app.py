import streamlit as st
import pandas as pd
from lib.firebase_client import get_approved_jobs

st.set_page_config(page_title="BioAgri Careers", page_icon="🌱", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stButton > button {
        border-radius: 8px; border: none; background-color: #2E7D32;
        color: white; font-weight: 600; padding: 0.5rem 1.5rem;
    }
    h1, h2, h3 { color: #1B5E20; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 BioAgri Careers")
st.subheader("Jobs, internships & scholarships for Biology and Agriculture students in Pakistan")

st.write(
    "Find opportunities in botany, agronomy, biotechnology, environmental science, "
    "and more — or post a listing if you're hiring or offering a scholarship."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/1_Browse_Jobs.py", label="💼 Jobs / 🎓 Scholarships", icon="🔍")
with col2:
    st.page_link("pages/3_Post_a_Job.py", label="📝 Post a listing", icon="📝")
with col3:
    st.page_link("pages/8_Blog.py", label="📰 Blog", icon="📰")
with col4:
    st.page_link("pages/4_My_Account.py", label="👤 My account", icon="👤")

st.divider()

st.subheader("📋 Latest listings")

try:
    jobs = get_approved_jobs()
    if not jobs:
        st.info("No approved listings yet — check back soon, or be the first to post one.")
    else:
        jobs_sorted = sorted(jobs, key=lambda j: j.get("createdAt") or 0, reverse=True)
        for job in jobs_sorted[:5]:
            badge = "🎓" if job.get("jobType") == "Scholarship" else "💼"
            with st.container(border=True):
                st.markdown(f"**{badge} {job.get('title')}** — {job.get('organization')}")
                st.caption(f"{job.get('category')} · {job.get('jobType')} · {job.get('location')}")
except Exception as e:
    st.warning("Couldn't load listings right now.")

st.divider()
st.caption("BioAgri Careers — connecting Biology & Agriculture talent with opportunities.")
