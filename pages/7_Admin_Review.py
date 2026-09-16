import streamlit as st
from lib.firebase_client import get_all_jobs, update_job_status

st.set_page_config(page_title="Admin Review · BioAgri Careers", page_icon="🔒", layout="wide")

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔒 Admin Access Required")
    password = st.text_input("Enter admin password", type="password")
    if st.button("Unlock"):
        if password == st.secrets.get("admin_password"):
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

st.title("🔒 Review Listings")

try:
    jobs = get_all_jobs()
except Exception as e:
    st.error(f"Could not load listings: {e}")
    st.stop()

pending = [j for j in jobs if j.get("status") == "Pending"]
approved = [j for j in jobs if j.get("status") == "Approved"]
rejected = [j for j in jobs if j.get("status") == "Rejected"]

st.caption(f"Pending: {len(pending)} · Approved: {len(approved)} · Rejected: {len(rejected)}")

tab1, tab2, tab3 = st.tabs([f"Pending ({len(pending)})", f"Approved ({len(approved)})", f"Rejected ({len(rejected)})"])

def render_job(job, show_actions=True):
    with st.container(border=True):
        st.markdown(f"### {job.get('title')}")
        st.caption(f"{job.get('organization')} · {job.get('category')} · {job.get('jobType')} · {job.get('location')}")
        st.write(job.get("description", ""))
        st.markdown(f"**Requirements:** {job.get('requirements', 'N/A')}")
        st.markdown(f"**Contact:** {job.get('contact', 'N/A')}")
        st.caption(f"Posted by: {job.get('posterEmail', 'Unknown')}")

        if show_actions:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"approve_{job['id']}"):
                    update_job_status(job["id"], "Approved")
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"reject_{job['id']}"):
                    update_job_status(job["id"], "Rejected")
                    st.rerun()

with tab1:
    if not pending:
        st.info("No pending listings.")
    for job in pending:
        render_job(job)

with tab2:
    if not approved:
        st.info("No approved listings.")
    for job in approved:
        render_job(job, show_actions=False)

with tab3:
    if not rejected:
        st.info("No rejected listings.")
    for job in rejected:
        render_job(job, show_actions=False)

if st.button("🔒 Lock again"):
    st.session_state.admin_authenticated = False
    st.rerun()
