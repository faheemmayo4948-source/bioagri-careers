import requests
import streamlit as st

API_KEY = None


def _get_api_key():
    global API_KEY
    if API_KEY is None:
        API_KEY = st.secrets["firebase_web_api_key"]
    return API_KEY


def sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={_get_api_key()}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload, timeout=15)
    data = response.json()
    if response.status_code != 200:
        raise RuntimeError(data.get("error", {}).get("message", "Sign up failed"))
    return data


def sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={_get_api_key()}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload, timeout=15)
    data = response.json()
    if response.status_code != 200:
        raise RuntimeError(data.get("error", {}).get("message", "Sign in failed"))
    return data
