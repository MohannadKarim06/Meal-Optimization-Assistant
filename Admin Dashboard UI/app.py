import streamlit as st
import requests
import os 

API_URL = os.getenv("BASE_API_KEY")  

st.set_page_config(page_title="Admin Dashboard", layout="centered")
st.title("📂 Admin Dashboard")


# --- FILE MANAGEMENT ---
st.header("📁 Uploaded PDFs")

# Load file list
with st.spinner("Loading file list..."):
    try:
        res = requests.get(f"{API_URL}/files")
        file_list = res.json()["files"]
    except Exception as e:
        st.error("Failed to load files. Check API logs.")
        file_list = []

# File uploader
uploaded_file = st.file_uploader("Upload a new PDF", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Uploading..."):
        try:
            res = requests.post(
                f"{API_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
            )
            if res.status_code == 200:
                st.success(res.json()["message"])
                st.experimental_rerun()
            else:
                st.error(f"Upload failed: {res.json()['detail']}")
        except Exception as e:
            st.error("Upload failed. Check API logs.")

# Delete file
if file_list:
    st.subheader("🗑️ Delete a file")
    file_to_delete = st.selectbox("Choose file to delete", file_list)
    if st.button("Delete File"):
        with st.spinner("Deleting..."):
            try:
                res = requests.delete(f"{API_URL}/delete/{file_to_delete}")
                if res.status_code == 200:
                    st.success(res.json()["message"])
                    st.experimental_rerun()
                else:
                    st.error(f"Delete failed: {res.json()['detail']}")
            except Exception as e:
                st.error("Delete failed. Check API logs.")


# --- CONFIGURATION MANAGEMENT ---
with st.expander("⚙️ Config Editor (click to expand)"):
    st.header("Configuration Settings")

    # Load current config
    try:
        config = requests.get(f"{API_URL}/config").json()
    except Exception as e:
        st.error("Failed to load config. Check API.")
        config = {}

    editable_keys = [
        "chat_model_name",
        "embedding_model_name",
        "base_prompt",
        "top_k_results",
        "token_limit",
    ]

    updated_config = {}

    for key in editable_keys:
        if key not in config:
            continue
        val = config[key]

        if isinstance(val, str):
            new_val = st.text_area(key, val, height=200 if key == "base_prompt" else 50)
        elif isinstance(val, int):
            new_val = st.number_input(key, value=val)
        else:
            continue

        if new_val != val:
            updated_config[key] = new_val

    if updated_config:
        if st.button("Update Config"):
            with st.spinner("Updating..."):
                try:
                    res = requests.post(f"{API_URL}/config", json=updated_config)
                    if res.status_code == 200:
                        st.success("Config updated!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Update failed: {res.json()['detail']}")
                except Exception as e:
                    st.error("Failed to update config. Check API logs.")


# --- LOG VIEWER ---
with st.expander("📜 View Logs (click to expand)"):
    if st.button("Load Logs"):
        with st.spinner("Fetching logs..."):
            try:
                res = requests.get(f"{API_URL}/logs")
                if res.status_code == 200:
                    st.text_area("Logs", res.json()["logs"], height=400)
                else:
                    st.error(f"Failed to fetch logs: {res.json()['detail']}")
            except Exception as e:
                st.error("Error fetching logs. Check API logs.")
