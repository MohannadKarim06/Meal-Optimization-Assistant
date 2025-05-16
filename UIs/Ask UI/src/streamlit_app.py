import os
os.environ["STREAMLIT_TELEMETRY"] = "0"
os.environ["STREAMLIT_DISABLE_USAGE_STATS"] = "true"
os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp"

import streamlit as st
import requests
import base64
import datetime

API_URL = os.getenv("API_BASE")

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
        st.error("Failed to load files. Check logs.")
        file_list = []

# File uploader
uploaded_file = st.file_uploader("Upload a new PDF", type=["pdf"])
if uploaded_file is not None:
    if st.button("Upload File"):
        with st.spinner("Uploading..."):
            try:
                res = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                )
                
                st.success(res.json()["message"])
                
            except Exception as e:
                st.error("Upload failed. Check logs.")


# Delete file
if file_list:
    st.subheader("🗑️ Delete a file")
    file_to_delete = st.selectbox("Choose file to delete", file_list)
    if st.button("Delete File"):
        with st.spinner("Deleting..."):
            try:
                res = requests.delete(f"{API_URL}/delete/{file_to_delete}")
                st.success(res.json()["message"])

            except Exception as e:
                st.error("Delete failed. Check logs.")

# --- CONFIGURATION MANAGEMENT ---
with st.expander("⚙️ Config Editor (click to expand)"):
    st.header("Configuration Settings")

    # Load current config
    try:
        config = requests.get(f"{API_URL}/config").json()
    except Exception as e:
        st.error("Failed to load config. Check Logs.")
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
            new_val = st.text_area(key, val, height=200 if key == "base_prompt" else 70)
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
                    st.success("Config updated!")
                    
                except Exception as e:
                    st.error("Failed to update config. Check API logs.")


# --- LOG VIEWER ---
with st.expander("📜 View Logs (click to expand)"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Load Logs"):
            with st.spinner("Fetching logs..."):
                try:
                    res = requests.get(f"{API_URL}/logs")
                    log_content = res.json()["logs"]
                    st.session_state.logs = log_content
                    st.text_area("Logs", log_content, height=400)
                    
                except Exception as e:
                    st.error("Error fetching logs. Check logs.")
                    st.session_state.logs = None
    
    # Download logs button
    with col2:
        if st.button("Download Logs"):
            if 'logs' in st.session_state and st.session_state.logs:
                log_content = st.session_state.logs
                
                # Create timestamp for filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs_{timestamp}.txt"
                
                # Create download link
                b64 = base64.b64encode(log_content.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download log file</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                with st.spinner("Fetching logs for download..."):
                    try:
                        res = requests.get(f"{API_URL}/logs")
                        log_content = res.json()["logs"]
                        
                        # Create timestamp for filename
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"logs_{timestamp}.txt"
                        
                        # Create download link
                        b64 = base64.b64encode(log_content.encode()).decode()
                        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download log file</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error("Error downloading logs. Check logs.")