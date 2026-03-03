"""
Chain-field chatbot UI: select Solana or EVM, then chat. Calls backend POST /chat.
"""
import os
import streamlit as st
import httpx

BACKEND_URL = os.getenv("CHATBOT_BACKEND_URL", "http://127.0.0.1:8000")

FIELD_OPTIONS = ["Solana", "EVM"]
FIELD_TO_API = {"Solana": "solana", "EVM": "evm"}


def check_backend():
    """Return True if backend is reachable."""
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=2.0)
        return r.status_code == 200
    except Exception:
        return False


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def send_message(field: str, message: str) -> str:
    api_field = FIELD_TO_API[field]
    with httpx.Client(timeout=60.0) as client:
        r = client.post(
            f"{BACKEND_URL}/chat",
            json={"field": api_field, "message": message},
        )
        r.raise_for_status()
        return r.json()["reply"]


def main():
    st.set_page_config(page_title="Chain-Field Chatbot", page_icon="💬", layout="centered")
    init_session()

    st.title("Chain-Field Chatbot")
    st.caption("Ask questions about Solana or EVM. Select the chain field below.")

    with st.sidebar:
        st.caption("Backend")
        if check_backend():
            st.success("API connected")
        else:
            st.error("Backend not running")
            st.markdown(
                "Start the API in another terminal:\n\n"
                "```\n"
                "cd E:\\Chupacabra\\Projects\\AI\\LLM\n"
                ".venv\\Scripts\\Activate.ps1\n"
                "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000\n"
                "```"
            )

    field = st.selectbox("Chain field", FIELD_OPTIONS, key="field")

    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Your message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = None
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = send_message(field, prompt)
                    st.markdown(reply)
                except httpx.HTTPStatusError as e:
                    st.error(f"API error: {e.response.status_code} - {e.response.text}")
                except httpx.ConnectError:
                    st.error(
                        "Cannot connect to the backend. Start it in another terminal with:\n\n"
                        "`uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`"
                    )
                except Exception as e:
                    st.error(str(e))
        if reply:
            st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
