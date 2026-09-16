import streamlit as st
from lib.auth_client import sign_up, sign_in

st.set_page_config(page_title="My Account · BioAgri Careers", page_icon="👤")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    st.title("👤 My Account")
    st.write(f"Logged in as: **{st.session_state.user['email']}**")
    st.page_link("pages/3_Post_a_Job.py", label="📝 Post a job", icon="📝")
    st.page_link("pages/6_My_Postings.py", label="📂 My postings", icon="📂")
    if st.button("Log out"):
        st.session_state.user = None
        st.rerun()
else:
    st.title("👤 Account")
    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In", type="primary"):
            try:
                result = sign_in(email, password)
                st.session_state.user = {"email": result["email"], "uid": result["localId"]}
                st.success("Logged in!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

    with tab2:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
        if st.button("Sign Up", type="primary"):
            try:
                result = sign_up(new_email, new_password)
                st.session_state.user = {"email": result["email"], "uid": result["localId"]}
                st.success("Account created!")
                st.rerun()
            except Exception as e:
                st.error(f"Sign up failed: {e}")
