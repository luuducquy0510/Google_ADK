import streamlit as st
import requests
import json

# URL to your FastAPI backend
BACKEND_URL= "http://localhost:8080"


# Chatbot section
st.set_page_config(page_title="Personal Assistant Assistant", page_icon="🧠")
st.title("Personal Assistant Assistant")

                    

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your research question..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build full conversation history (excluding current prompt)
    full_prompt = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages]
    )

    payload = {"query": full_prompt}
    # Show assistant message streaming
    with st.chat_message("assistant"):
        output_box = st.empty()
        streamed_reply = ""

        # Send request with stream=True
        with requests.post(
            f"{BACKEND_URL}/conversation",
            json=payload,
            stream=True,
        ) as res:
            res.raise_for_status()

            for chunk in res.iter_content(chunk_size=1):
                if chunk:
                    streamed_reply += chunk.decode("utf-8", errors="ignore")
        response_obj = json.loads(streamed_reply)
        response_text = response_obj["response"]

        output_box.markdown(response_text)


    # Save assistant message to history
    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )


