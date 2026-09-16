import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


def _init_app():
    if not firebase_admin._apps:
        service_account_info = dict(st.secrets["firebase_service_account"])
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()


def get_db():
    _init_app()
    return firestore.client()


# --- Jobs / Internships / Scholarships ---

def post_job(title, organization, category, job_type, location, description,
             requirements, deadline, contact, funding=None, poster_uid=None, poster_email=None):
    db = get_db()
    db.collection("jobs").add({
        "title": title,
        "organization": organization,
        "category": category,
        "jobType": job_type,
        "location": location,
        "description": description,
        "requirements": requirements,
        "deadline": deadline,
        "contact": contact,
        "funding": funding,
        "status": "Pending",
        "posterUid": poster_uid,
        "posterEmail": poster_email,
        "createdAt": firestore.SERVER_TIMESTAMP,
    })


def get_approved_jobs():
    db = get_db()
    docs = db.collection("jobs").where("status", "==", "Approved").stream()
    jobs = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        jobs.append(data)
    return jobs


def get_all_jobs():
    db = get_db()
    docs = db.collection("jobs").stream()
    jobs = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        jobs.append(data)
    return jobs


def get_jobs_by_poster(uid):
    db = get_db()
    docs = db.collection("jobs").where("posterUid", "==", uid).stream()
    jobs = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        jobs.append(data)
    return jobs


def update_job_status(job_id, new_status):
    db = get_db()
    db.collection("jobs").document(job_id).update({"status": new_status})


# --- Blog ---

def create_blog_post(title, content, category, image_url, author_email):
    db = get_db()
    db.collection("blog_posts").add({
        "title": title,
        "content": content,
        "category": category,
        "imageUrl": image_url,
        "authorEmail": author_email,
        "createdAt": firestore.SERVER_TIMESTAMP,
    })


def get_blog_posts():
    db = get_db()
    docs = db.collection("blog_posts").stream()
    posts = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        posts.append(data)
    return posts


def add_comment(post_id, user_email, comment_text):
    db = get_db()
    db.collection("blog_posts").document(post_id).collection("comments").add({
        "userEmail": user_email,
        "text": comment_text,
        "createdAt": firestore.SERVER_TIMESTAMP,
    })


def get_comments(post_id):
    db = get_db()
    docs = (
        db.collection("blog_posts").document(post_id)
        .collection("comments").order_by("createdAt").stream()
    )
    comments = []
    for doc in docs:
        data = doc.to_dict()
        comments.append(data)
    return comments
