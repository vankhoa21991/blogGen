import streamlit as st
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
load_dotenv()
import os


# FastAPI server endpoint for exchanging `auth_code` with access token
API_BASE_URL = os.getenv("API_BASE_URL")
LOGIN_URL=os.getenv("LOGIN_URL")
SIGNUP_URL=os.getenv("SIGNUP_URL")

st.write("Please log in to continue:")
st.markdown(F'<a href="{LOGIN_URL}" target="_self">Log In with Google</a>', unsafe_allow_html=True)
st.markdown(F'<a href="{SIGNUP_URL}" target="_self">Sign Up with Google</a>', unsafe_allow_html=True)

# Capture the access and refresh tokens from the URL query parameters
query_params = st.experimental_get_query_params()
access_token = query_params.get("access_token", [None])[0]
refresh_token = query_params.get("refresh_token", [None])[0]

if access_token and refresh_token:
    # Store tokens in Streamlit session state
    st.session_state["jwt"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.success("Successfully logged in!")

else:
    st.info("Please log in.")

# Store tokens in session state
if "jwt" not in st.session_state:
    st.session_state["jwt"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None


# Button to call unprotected API
if st.button("Call Unprotected API"):
    response = requests.get(f"{API_BASE_URL}/api/")
    st.write("Response:", response.json())

# Button to call protected API without JWT
if st.button("Call Protected API without JWT"):
    response = requests.get(f"{API_BASE_URL}/api/protected")
    st.write("Response:", response.json())

# Button to call protected API with JWT
if st.button("Call Protected API with JWT"):
    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
    response = requests.get(f"{API_BASE_URL}/api/protected", headers=headers)
    st.write("Response:", response.json())

# Button to logout
if st.button("Logout"):
    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
    response = requests.get(f"{API_BASE_URL}/logout", headers=headers)
    if response.status_code == 200 and response.json().get("result"):
        st.session_state["jwt"] = None
        st.session_state["refresh_token"] = None
        st.success("Logged out successfully.")
    else:
        st.error("Logout failed.")

# Button to refresh JWT token
if st.button("Refresh"):
    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
    data = {"grant_type": "refresh_token", "refresh_token": st.session_state["refresh_token"]}
    response = requests.post(f"{API_BASE_URL}/auth/refresh", headers=headers, json=data)
    if response.status_code == 200:
        tokens = response.json()
        st.session_state["jwt"] = tokens["access_token"]
        st.success("Token refreshed!")
    else:
        st.error("Failed to refresh token.")