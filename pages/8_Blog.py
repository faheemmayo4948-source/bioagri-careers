import streamlit as st
from lib.firebase_client import get_blog_posts, add_comment, get_comments

st.set_page_config(page_title="Blog · BioAgri Careers", page_icon="📰", layout="wide")

if "selected_post" not in st.session_state:
    st.session_state.selected_post = None

try:
    posts = get_blog_posts()
except Exception as e:
    st.error(f"Could not load blog posts: {e}")
    st.stop()

posts_sorted = sorted(posts, key=lambda p: p.get("createdAt") or 0, reverse=True)

# --- Detail view ---
if st.session_state.selected_post:
    post = next((p for p in posts_sorted if p["id"] == st.session_state.selected_post), None)

    if post is None:
        st.session_state.selected_post = None
        st.rerun()

    if st.button("← Back to all posts"):
        st.session_state.selected_post = None
        st.rerun()

    st.title(post.get("title"))
    st.caption(f"{post.get('category')} · by {post.get('authorEmail', 'BioAgri Careers')}")
    if post.get("imageUrl"):
        st.image(post["imageUrl"], use_container_width=True)
    st.write(post.get("content"))

    st.divider()
    st.subheader("💬 Comments")

    comments = get_comments(post["id"])
    if not comments:
        st.caption("No comments yet — be the first to comment.")
    for c in comments:
        with st.container(border=True):
            st.markdown(f"**{c.get('userEmail', 'Anonymous')}**")
            st.write(c.get("text"))

    st.divider()
    if "user" not in st.session_state or not st.session_state.user:
        st.info("Please log in to leave a comment.")
        st.page_link("pages/4_My_Account.py", label="👤 Go to Account page", icon="👤")
    else:
        comment_text = st.text_area("Add a comment", key="new_comment")
        if st.button("Post comment", type="primary"):
            if comment_text.strip():
                add_comment(post["id"], st.session_state.user["email"], comment_text.strip())
                st.rerun()
            else:
                st.warning("Comment can't be empty.")

# --- List view ---
else:
    st.title("📰 Blog")
    st.caption("Career tips, scholarship guides, and advice for Biology & Agriculture students.")

    if not posts_sorted:
        st.info("No blog posts yet — check back soon.")
    else:
        categories = ["All categories"] + sorted({p.get("category", "General") for p in posts_sorted})
        category_filter = st.selectbox("Filter by category", categories)

        filtered = posts_sorted if category_filter == "All categories" else [
            p for p in posts_sorted if p.get("category") == category_filter
        ]

        cols = st.columns(2)
        for i, post in enumerate(filtered):
            with cols[i % 2]:
                with st.container(border=True):
                    if post.get("imageUrl"):
                        st.image(post["imageUrl"], use_container_width=True)
                    st.markdown(f"### {post.get('title')}")
                    st.caption(post.get("category"))
                    preview = (post.get("content") or "")[:150]
                    st.write(preview + ("..." if len(post.get("content", "")) > 150 else ""))
                    if st.button("Read more", key=f"read_{post['id']}"):
                        st.session_state.selected_post = post["id"]
                        st.rerun()
