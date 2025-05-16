import streamlit as st
import requests
import os

API_URL = os.getenv("API_BASE")

st.set_page_config(page_title="Ask a Question", layout="centered")
st.title("sweetreactions.ai\nby Karan Sarin")

st.markdown(
    "Drop any meal and i will show you how to crush the glucose spike, while keeping all the flavor 🔥"
)

# Initialize session state for history
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# Sidebar for question history
with st.sidebar:
    st.header("📜 Question History")
    if st.session_state.qa_history:
        for i, item in enumerate(reversed(st.session_state.qa_history), 1):
            with st.expander(f"Q{i}: {item['question']}"):
                st.write(f"**A:** {item['answer']}")
    else:
        st.caption("No questions asked yet.")

# Input area
question = st.text_input("Enter your question below:")

if st.button("Submit Question") and question.strip():
    with st.spinner("Getting an answer..."):
        try:
            # Pass query as a query parameter
            res = requests.post(f"{API_URL}/ask?query={question}")
            if res.status_code == 200:
                answer = res.json()["response"]
                st.success("Answer:")
                st.write(answer)
                # Add to session history
                st.session_state.qa_history.append({"question": question, "answer": answer})
            else:
                st.error(f"Error, Please check logs.")
        except Exception as e:
            st.error("Failed to connect to the backend. Please check the logs and try again.")