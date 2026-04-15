import streamlit as st
import json
import os

st.title("🔍 TrackBack - Lost & Found System")
st.markdown("### 🚀 Find your lost items quickly and easily")

# -----------------------------
# Functions for storage
# -----------------------------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def match_score(lost_name, found_name):
    lost_words = set(lost_name.lower().split())
    found_words = set(found_name.lower().split())
    common = lost_words.intersection(found_words)
    score = len(common) / max(len(lost_words), 1)
    return int(score * 100)

# Load data
lost_items = load_data("lost.json")
found_items = load_data("found.json")

# -----------------------------
# Menu
# -----------------------------
option = st.sidebar.selectbox(
    "Choose Option",
    ["Report Lost Item", "Report Found Item", "View All Items"]
)

# -----------------------------
# Report Lost Item
# -----------------------------
if option == "Report Lost Item":
    st.header("📌 Report Lost Item")

    name = st.text_input("Item Name")
    location = st.text_input("Last Seen Location")
    description = st.text_area("Description")
    contact = st.text_input("Your Contact (Phone/Email)")
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Submit Lost Item"):
        lost_items.append({
            "name": name,
            "location": location,
            "description": description,
            "contact": contact
        })
        save_data("lost.json", lost_items)
        st.success("Lost item reported!")

# -----------------------------
# Report Found Item
# -----------------------------
elif option == "Report Found Item":
    st.header("📌 Report Found Item")

    name = st.text_input("Item Name")
    location = st.text_input("Found Location")
    description = st.text_area("Description")
    contact = st.text_input("Your Contact (Phone/Email)")
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Submit Found Item"):
        found_items.append({
            "name": name,
            "location": location,
            "description": description,
            "contact": contact
        })
        save_data("found.json", found_items)
        st.success("Found item reported!")

# -----------------------------
# View Items + Matching
# -----------------------------
elif option == "View All Items":
    st.header("📋 All Items")

    st.subheader("🔴 Lost Items")
    for item in lost_items:
        st.info(f"Item: {item['name']} | Location: {item['location']} | Contact: {item['contact']}")

    st.subheader("🟢 Found Items")
    for item in found_items:
        st.info(f"Item: {item['name']} | Location: {item['location']} | Contact: {item['contact']}")

    st.subheader("🤖 Matching Results")
    for lost in lost_items:
        for found in found_items:
            if any(word in found["name"].lower() for word in lost["name"].lower().split()):
                st.success(f"Match Found: {lost['name']} ↔ {found['name']}")

    st.subheader("🤖 Matching Results")
for lost in lost_items:
    for found in found_items:
        score = match_score(lost["name"], found["name"])
        if score > 0:
            st.success(f"Match Found: {lost['name']} ↔ {found['name']} (Match: {score}%)")
            