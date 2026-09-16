import requests
import streamlit as st


def upload_image(file_bytes, file_name):
    """Upload an image to Cloudinary using an unsigned upload preset."""
    cloud_name = st.secrets["cloudinary_cloud_name"]
    upload_preset = st.secrets["cloudinary_upload_preset"]

    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"

    files = {"file": (file_name, file_bytes)}
    data = {"upload_preset": upload_preset}

    response = requests.post(url, files=files, data=data, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(f"Cloudinary upload failed: {response.text}")

    return response.json()["secure_url"]
