import os
import streamlit as st
import requests

# ⚠️ CHANGE THIS URL to your RENDER or LOCALHOST URL or set env var API_URL
# Default to localhost for local development
#API_URL = "http://resume-compare.duckdns.org:8000"
API_URL = "http://127.0.0.1:8000"
st.title("📄 AI Resume Comparison System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- SIGNUP ---
def signup_ui():
    st.subheader("📝 Signup")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["student", "admin"])

    if st.button("Signup"):
        res = requests.post(
            f"{API_URL}/signup",
            data={"username": username, "password": password, "role": role}
        )
        try:
            st.write(res.json())
        except Exception:
            st.error("Server Error: Received HTML instead of JSON. Check API_URL.")
            st.code(res.text[:500])

# Use the internal loopback address, NOT the public DuckDNS URL
API_URL = "http://127.0.0.1:8000"

def login_ui():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            # The backend lives on the same machine, so we talk to localhost
            res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.success("Login Successful!")
            else:
                st.error("Login failed.")
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")

# Main app logic...
# # --- LOGIN ---
# def login_ui():
#     st.subheader("🔐 Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         res = requests.post(
#             f"{API_URL}/login",
#             data={"username": username, "password": password}
#         )
#         try:
#             data = res.json()
#             if data.get("message") == "Login success":
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.session_state.role = data["role"]
#                 st.success("Login successful")
#                 st.rerun()
#             else:
#                 st.error(data.get("message", "Invalid credentials"))
#         except Exception:
#             st.error("Login failed. Server returned non-JSON response.")

# --- STUDENT DASHBOARD ---
def student_dashboard():
    st.header("🎓 Student Dashboard")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf","docx"])

    if uploaded_file and st.button("Upload Resume"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        data = {"username": st.session_state.username}
        res = requests.post(f"{API_URL}/upload_student", files=files, data=data)
        st.write(res.json())

    st.divider()

    if st.button("Compare Resume"):
        res = requests.post(f"{API_URL}/compare", data={"username": st.session_state.username})
        try:
            result = res.json()
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("📊 Resume Analysis")
                st.metric("Similarity Score", result.get('Similarity Percentage', '0%'))
                st.metric("Skill Match", result.get('Skill Match Percentage', '0%'))
                st.write("### Matched Skills", result.get("Matched Skills", []))
                st.write("### Verdict", result.get("Overall Verdict", "N/A"))
        except Exception:
            st.error("Comparison failed. Check if Backend is running.")

# --- ADMIN DASHBOARD ---
def admin_dashboard():
    st.header("🧑‍💼 Admin Dashboard")
    uploaded_file = st.file_uploader("Upload Job Description", type=["pdf","docx"])
    if uploaded_file and st.button("Upload Job Description"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        res = requests.post(f"{API_URL}/upload_admin", files=files)
        st.write(res.json())

# --- MAIN UI ---
menu = st.sidebar.selectbox("Menu", ["Login","Signup"])

if not st.session_state.logged_in:
    if menu == "Login": login_ui()
    else: signup_ui()
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.session_state.role == "student": student_dashboard()
    else: admin_dashboard()
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
