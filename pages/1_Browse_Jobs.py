import streamlit as st
from lib.firebase_client import get_approved_jobs

st.set_page_config(page_title="Browse · BioAgri Careers", page_icon="🔍", layout="wide")

st.title("🔍 Browse Listings")

try:
    all_jobs = get_approved_jobs()
except Exception as e:
    st.error(f"Could not load listings: {e}")
    st.stop()

if not all_jobs:
    st.info("No approved listings yet.")
    st.stop()

tab1, tab2 = st.tabs(["💼 Jobs & Internships", "🎓 Scholarships"])


def render_listings(jobs, search_key):
    if not jobs:
        st.info("No listings in this category yet.")
        return

    col1, col2 = st.columns(2)
    with col1:
        categories = ["All categories"] + sorted({j.get("category", "Other") for j in jobs})
        category_filter = st.selectbox("Category", categories, key=f"cat_{search_key}")
    with col2:
        search = st.text_input("Search by keyword", placeholder="e.g. Lahore, research", key=f"search_{search_key}")

    filtered = jobs
    if category_filter != "All categories":
        filtered = [j for j in filtered if j.get("category") == category_filter]
    if search:
        s = search.lower()
        filtered = [j for j in filtered if s in " ".join(str(v) for v in j.values()).lower()]

    st.caption(f"Showing {len(filtered)} of {len(jobs)} listings")

    for job in sorted(filtered, key=lambda j: j.get("createdAt") or 0, reverse=True):
        with st.container(border=True):
            st.markdown(f"### {job.get('title')}")
            st.caption(f"**{job.get('organization')}** · {job.get('category')} · {job.get('jobType')} · {job.get('location')}")
            if job.get("funding"):
                st.info(f"💰 Funding: {job.get('funding')}")
            st.write(job.get("description", ""))

            with st.expander("Requirements & how to apply"):
                st.markdown(f"**Requirements/Eligibility:** {job.get('requirements', 'Not specified')}")
                if job.get("deadline"):
                    st.markdown(f"**Deadline:** {job.get('deadline')}")
                contact = job.get("contact", "")
                if contact.startswith("http"):
                    st.link_button("Apply / Learn more", contact)
                elif "@" in contact:
                    st.markdown(f"**Apply via email:** {contact}")
                else:
                    st.markdown(f"**Contact:** {contact}")


with tab1:
    jobs_only = [j for j in all_jobs if j.get("jobType") != "Scholarship"]
    render_listings(jobs_only, "jobs")

with tab2:
    scholarships_only = [j for j in all_jobs if j.get("jobType") == "Scholarship"]
    render_listings(scholarships_only, "scholarships")
