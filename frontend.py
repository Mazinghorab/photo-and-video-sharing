import streamlit as st
import requests

API_URL = "http://localhost:8000"

if "token" not in st.session_state:
  st.session_state.token = None
if "user" not in st.session_state:
  st.session_state.user = None

def get_headers():
  if st.session_state.token:
    return {"Authorization": f"Bearer {st.session_state.token}"}
  return {}

st.sidebar.title("Authentication")
auth_mode = st.sidebar.radio("Mode", ["Login", "Register"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if auth_mode == "Register":
  if st.sidebar.button("Sign Up"):
    resp = requests.post(f"{API_URL}/auth/register", json={
      "email": email,
      "password": password,
      "is_active": True,
      "is_superuser": False,
      "is_verified": False
    })
    if resp.status_code == 201:
      st.sidebar.success("Registered successfully! You can now log in.")
    else:
      st.sidebar.error("Registration failed. Please try again.")

elif auth_mode == "Login":
  if st.sidebar.button("Log In"):
    resp = requests.post(f"{API_URL}/auth/jwt/login", data={
      "username": email,
      "password": password
    })
    if resp.status_code == 200:
      st.session_state.token = resp.json().get("access_token")
      user_resp = requests.get(f"{API_URL}/users/me", headers=get_headers())
      if user_resp.status_code == 200:
        st.session_state.user = user_resp.json()
        st.sidebar.success("Logged in successfully!")
        st.rerun()
    else:
      st.sidebar.error("Invalid credentials.")

if st.session_state.token:
  if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()

if st.session_state.token:
  st.title("Photo & Video Sharing App")
  tab1, tab2 = st.tabs(["Feed", "Upload"])
  with tab1:
    st.header("Feed")
    feed_resp = requests.get(f"{API_URL}/feed", headers=get_headers())
    if feed_resp.status_code == 200:
      feed_data = feed_resp.json()
      posts = feed_data.get("posts", []) if isinstance(feed_data, dict) else feed_data
      for post in posts:
        st.subheader(f"Posted by {post['user_id']}")
        st.caption(f"Created at: {post['created_at']}")
        media_url = post['url']
        caption_text = post['caption']
        if post['file_type'] == "image":
          transformed_url = f"{media_url}?tr=l-text,i-{caption_text},fs-100,l-end"
          st.image(transformed_url)
        else:
          st.video(media_url)
          st.write(f"**Caption:** {caption_text}")
        if post.get('is_owner'):
          if st.button(f"Delete Post", key=post['id']):
            del_resp = requests.delete(f"{API_URL}/post/{post['id']}", headers=get_headers())
            if del_resp.status_code == 200:
              st.success("Post deleted successfully!")
              st.rerun()
            else:
              st.error("Failed to delete post.")
        st.markdown("---")
    else:
      st.error("Failed to load feed.")

  with tab2:
    st.header("Upload New Post")
    uploaded_file = st.file_uploader("Choose an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])
    caption = st.text_input("Caption")
    if st.button("Share"):
      if uploaded_file and caption:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"caption": caption}
        with st.spinner("Uploading to ImageKit..."):
          upload_resp = requests.post(f"{API_URL}/upload", files=files, data=data, headers=get_headers())
          if upload_resp.status_code == 200:
            st.success("Uploaded successfully!")
          else:
            st.error(f"Failed to upload: {upload_resp.text}")
      else:
        st.warning("Please select a file and enter a caption.")

else:
  st.title("Welcome to the App")
  st.info("Please sign up or log in from the sidebar to view the feed and upload posts.")