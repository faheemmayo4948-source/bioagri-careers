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


def post_job(title, organization, category, job_type, location, description,
             requirements, deadline, contact, poster_uid=None, poster_email=None):
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
