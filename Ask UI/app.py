import streamlit as st
import requests
import os

API_URL = os.getenv("BASE_API_KEY")  

st.set_page_config(page_title="Ask a Question", layout="centered")
st.title("❓ Ask a Question")

st.markdown(
    "This interface allows you to ask a one-time question based on your uploaded documents."
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
            res = requests.post(f"{API_URL}/ask", json={"query": question})
            if res.status_code == 200:
                answer = res.json()["answer"]
                st.success("Answer:")
                st.write(answer)
                # Add to session history
                st.session_state.qa_history.append({"question": question, "answer": answer})
            else:
                st.error(f"Error: {res.json().get('detail', 'Something went wrong.')}")
        except Exception as e:
            st.error("Failed to connect to the backend. Please check the logs and try again.")
