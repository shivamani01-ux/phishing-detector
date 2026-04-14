import streamlit as st

st.title("🔐 Phishing URL Detector")
st.markdown("---")
st.info("⚡ Detect whether a URL is safe or potentially phishing")

def check_url(url):
    score = 0
    reasons = []

    # Rule 1: HTTPS check
    if not url.startswith("https"):
        score += 1
        reasons.append("❌ URL is not secure (no HTTPS)")

    # Rule 2: Long URL
    if len(url) > 50:
        score += 1
        reasons.append("⚠️ URL is unusually long")

    # Rule 3: Suspicious keywords
    suspicious_words = ["login", "verify", "bank", "secure", "account", "update"]
    if any(word in url.lower() for word in suspicious_words):
        score += 1
        reasons.append("⚠️ Contains suspicious words")

    # Final result
    if score == 0:
        result = "Safe ✅"
    elif score == 1:
        result = "Suspicious ⚠️"
    else:
        result = "Dangerous ❌"

    return result, reasons

import streamlit as st
import requests

API_KEY = "PASTE_YOUR_API_KEY_HERE"

st.set_page_config(page_title="Phishing Detector", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>🔐 Phishing URL Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Check if a URL is safe using real-time security analysis</p>", unsafe_allow_html=True)
st.markdown("---")

def check_url_virustotal(url):
    headers = {"x-apikey": API_KEY}

    data = {"url": url}
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        return "Error", [], 0, 0

    url_id = response.json()["data"]["id"]

    analysis = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{url_id}",
        headers=headers
    )

    result_data = analysis.json()
    stats = result_data["data"]["attributes"]["stats"]

    malicious = stats["malicious"]
    suspicious = stats["suspicious"]

    if malicious > 0:
        result = "Dangerous ❌"
        color = "red"
    elif suspicious > 0:
        result = "Suspicious ⚠️"
        color = "orange"
    else:
        result = "Safe ✅"
        color = "green"

    return result, color, malicious, suspicious


# Input box
url = st.text_input("🔗 Enter URL to analyze:")

# Button
if st.button("🚀 Check URL"):
    if url:
        with st.spinner("Analyzing URL..."):
            result, color, malicious, suspicious = check_url_virustotal(url)

        # Result box
        st.markdown(
            f"<h2 style='color:{color}; text-align:center;'>Result: {result}</h2>",
            unsafe_allow_html=True
        )

        st.markdown("### 📊 Detailed Report")
        st.write(f"🔴 Malicious reports: {malicious}")
        st.write(f"🟠 Suspicious reports: {suspicious}")

    else:
        st.warning("⚠️ Please enter a URL")