
import streamlit as st
import pandas as pd
from datetime import datetime

from backend import model, database, ipcheck

st.set_page_config(page_title="Suspicious Login Detection", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login(username, password):
    return username == "admin" and password == "admin123"

if not st.session_state.authenticated:
    st.title("🔒 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.authenticated = True
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid credentials")
    st.stop()

st.title("🛡️ Suspicious Login Activity Monitor")

st.subheader("📥 New Login Record")

with st.form("login_form"):
    user_id = st.text_input("User ID")
    login_time = st.date_input("Login Time", datetime.now()).strftime("%Y-%m-%d")
    loc_score = st.slider("Location Score (0 = normal, 1 = suspicious)", 0.0, 1.0, 0.5)
    dev_score = st.slider("Device Score (0 = normal, 1 = suspicious)", 0.0, 1.0, 0.5)
    ip = st.text_input("IP Address")
    submitted = st.form_submit_button("Submit")

if submitted:
    database.store_login(user_id, login_time, loc_score, dev_score, ip)

    anomaly = model.detect_anomaly(user_id)
    threat_info = ipcheck.get_ip_threat_info(ip)
    geo_info = ipcheck.get_ip_location(ip)

    st.subheader("📊 Login Risk Analysis")
    st.write("Anomaly Detected:", "🔴 Yes" if anomaly else "🟢 No")
    st.write("Abuse Confidence Score:", threat_info["abuse_score"])
    st.write("Country (Threat DB):", threat_info["country"])
    st.write("Country (Geolocation):", geo_info["country"])

    st.expander("📄 Raw Threat Data").json(threat_info["full"])
    st.expander("📍 Raw Geolocation Data").json(geo_info["full"])

    st.subheader("🗺️ IP Location Map")
    st.map(pd.DataFrame([{"lat": geo_info["lat"], "lon": geo_info["lon"]}]))

st.subheader("📂 Login History")
df = pd.DataFrame(database.get_all_logins(), columns=["User ID", "Date", "Loc Score", "Dev Score", "IP"])
st.dataframe(df)
