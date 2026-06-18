import streamlit as st
import requests
from PyPDF2 import PdfReader

from auth import init_db, register, login


# -----------------------------
# INIT AUTH DB
# -----------------------------
init_db()


API_URL = "http://127.0.0.1:8000/analyze"


# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------------
# LOGIN PAGE
# -----------------------------
def auth_page():
    st.title("🔐 Login / Register")

    option = st.radio("Choose Action", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Register":
        if st.button("Create Account"):
            if register(username, password):
                st.success("Account created! Now login.")
            else:
                st.error("User already exists")

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")


# -----------------------------
# PDF EXTRACT
# -----------------------------
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():
    st.title("🚀 AI Resume Intelligence System")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    uploaded_file = st.file_uploader("Upload Resume PDF")
    jd_text = st.text_area("Job Description")

    if uploaded_file:

        resume_text = extract_text(uploaded_file)

        if st.button("Analyze Resume"):

            response = requests.post(
                API_URL,
                json={"text": resume_text, "jd": jd_text}
            ).json()

            st.metric("ATS Score", f"{response['ats_score']}%")
            st.metric("JD Match", f"{response['jd_score']}%")

            st.subheader("Roles")
            st.write(response["roles"])

            st.subheader("Skills")
            st.write(response["skills"])

            st.subheader("Missing Skills")
            st.write(response["missing"])


# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.logged_in:
    dashboard()
else:
    auth_page()