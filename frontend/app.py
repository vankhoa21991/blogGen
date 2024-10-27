import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
SIGNUP_URL = os.getenv("SIGNUP_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Custom CSS for the navigation bar and buttons
st.markdown("""
    <style>
    .top-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        background-color: #0d1117;
        padding: 10px;
        border-radius: 10px;
    }
    .top-bar > button {
        margin-left: 10px;
    }
    .content-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Store tokens in session state
if "jwt" not in st.session_state:
    st.session_state["jwt"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

# Display the navigation bar
st.markdown('<div class="navbar">', unsafe_allow_html=True)

# Check if user is logged in
query_params = st.query_params
access_token = query_params.get("access_token", [None]) if "access_token" in query_params else None
refresh_token = query_params.get("refresh_token", [None]) if "refresh_token" in query_params else None
name = query_params.get("name", [None]) if "name" in query_params else None

if "state" in query_params and query_params["state"] == "signup":
    st.info(f"No account found for {query_params['email']}. Please sign up.")
    del query_params["state"]

if access_token and refresh_token:
    st.session_state["jwt"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.session_state["name"] = name
    st.success("Successfully logged in!")
    # st.query_params  # Clear URL parameters
else:
    st.info("Please sign up or log in.")

# Display login/signup buttons if not logged in; otherwise, display logout
if "jwt" in st.session_state and st.session_state["jwt"] is not None:
    st.write(f"Welcome, {st.session_state['name']}!")
    logout_clicked = st.button("Logout")
    if logout_clicked:
        # Clear session state tokens
        st.session_state["jwt"] = None
        st.session_state["refresh_token"] = None
        access_token = None
        refresh_token = None
        st.success("Logged out successfully.")
        # Redirect to the login/signup page
        st.markdown(f'<meta http-equiv="refresh" content="0;url={FRONTEND_URL}">', unsafe_allow_html=True)

    
else:
    login_clicked = st.button("Log In")
    signup_clicked = st.button("Sign Up")

    if login_clicked:
        # Redirect user to the login page
        st.markdown(f'<meta http-equiv="refresh" content="0;url={LOGIN_URL}">', unsafe_allow_html=True)


    if signup_clicked:
        # Redirect user to the signup page
        st.markdown(f'<meta http-equiv="refresh" content="0;url={SIGNUP_URL}">', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("Welcome to My Blogging Application!")

# User Dashboard if logged in
if st.session_state["jwt"] is not None:
    st.subheader("User Dashboard")

    # Fetch and display the three most recent posts
    st.write("**Recent Posts:**")
    headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
    recent_posts = requests.get(f"{API_BASE_URL}/api/posts/recent", headers=headers)
    
    if recent_posts.status_code == 200:
        posts = recent_posts.json()
        for post in posts:
            st.write(f"**{post['user_name']}** at {post['created_at']}")
            st.write(post["content"])
            st.write("---")  # Divider between posts
    else:
        st.error("Failed to load recent posts.")


    st.write("Add a new post below:")
    
    content = st.text_area("Content")
    
    if st.button("Submit"):
        headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
        response = requests.post(f"{API_BASE_URL}/api/post", headers=headers, 
                                 json={"content": content})
        if response.status_code == 200:
            st.success("Post submitted successfully!")
        else:
            st.error("Failed to submit post.")


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
    print(headers)
    response = requests.get(f"{API_BASE_URL}/api/protected", headers=headers)
    st.write("Response:", response.json())

# add a button to show all users
# if st.button("Show all users"):
#     headers = {"Authorization": f"Bearer {st.session_state['jwt']}"}
#     response = requests.get(f"{API_BASE_URL}/api/users", headers=headers)
#     st.write("Response:", response.json())