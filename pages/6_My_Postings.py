import streamlit as st
from lib.firebase_client import get_jobs_by_poster

st.set_page_config(page_title="My Postings · BioAgri Careers", page_icon="📂")

st.title("📂 My Postings")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.page_link("pages/4_My_Account.py", label="👤 Go to Account page", icon="👤")
    st.stop()

uid = st.session_state.user["uid"]

try:
    jobs = get_jobs_by_poster(uid)
except Exception as e:
    st.error(f"Could not load your postings: {e}")
    st.stop()

if not jobs:
    st.info("You haven't posted any listings yet.")
    st.page_link("pages/3_Post_a_Job.py", label="📝 Post your first job", icon="📝")
else:
    for job in jobs:
        with st.container(border=True):
            status = job.get("status", "Pending")
            color = {"Approved": "🟢", "Pending": "🟡", "Rejected": "🔴"}.get(status, "⚪")
            st.markdown(f"### {job.get('title')} {color} *{status}*")
            st.caption(f"{job.get('organization')} · {job.get('category')} · {job.get('jobType')}")
