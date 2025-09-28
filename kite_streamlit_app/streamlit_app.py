import streamlit as st
import time
import traceback
import json
from typing import Any
import os

# MCP + strands imports
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp import MCPClient
from strands import Agent
from strands.models.openai import OpenAIModel

# --- Configuration ---
KITE_MCP_ENDPOINT = os.getenv("KITE_MCP_ENDPOINT", "https://mcp.kite.trade/mcp")

# --- Transport factory ---

def create_kite_transport():
    return streamablehttp_client(KITE_MCP_ENDPOINT)


# --- Helpers to extract and render agent responses ---

def extract_agent_text(result: Any) -> str:
    """
    Extract human-readable text from various agent return shapes.
    Handles strings, dicts, and AgentResult-like objects with .message or .messagedict.
    """
    # plain string
    if isinstance(result, str):
        return result

    # objects with attributes (AgentResult)
    msg = None
    try:
        msg = getattr(result, "message", None)
    except Exception:
        msg = None

    # fallback to dict-style access
    if msg is None:
        if isinstance(result, dict):
            msg = result.get("message") or result.get("messagedict") or result.get("content")

    # If msg is a dict containing 'content' which is often a list of text pieces
    content = None
    if isinstance(msg, dict):
        content = msg.get("content") or msg.get("content", None)

    # If we couldn't get message, maybe top-level result has 'content'
    if content is None and isinstance(result, dict):
        content = result.get("content")

    # Normalize content to a string
    texts = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and "text" in item:
                texts.append(item["text"])
            elif isinstance(item, str):
                texts.append(item)
            else:
                texts.append(json.dumps(item, default=str))
    elif isinstance(content, str):
        texts.append(content)
    elif msg and isinstance(msg, str):
        texts.append(msg)
    elif hasattr(result, "message") and isinstance(getattr(result, "message"), str):
        texts.append(getattr(result, "message"))
    else:
        try:
            texts.append(json.dumps(result, default=str))
        except Exception:
            texts.append(str(result))

    return "\n\n".join(texts).strip()


def render_agent_result(result: Any, show_metadata: bool = True, max_chars: int = 12000):
    """
    Renders the agent result in Streamlit as markdown, and shows metadata (stop_reason/metrics) in an expander.
    """
    text = extract_agent_text(result)

    truncated = False
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... (output truncated)"
        truncated = True

    # Render markdown
    st.markdown(text)

    # Try to collect metadata
    meta = {}
    try:
        stop_reason = getattr(result, "stop_reason", None)
        if stop_reason:
            meta["stop_reason"] = str(stop_reason)
    except Exception:
        pass

    try:
        metrics = getattr(result, "metrics", None)
        if metrics:
            meta["metrics"] = json.loads(json.dumps(metrics, default=str))
    except Exception:
        if isinstance(result, dict) and "metrics" in result:
            meta["metrics"] = result["metrics"]

    if meta and show_metadata:
        with st.expander("Agent metadata (stop reason / metrics)", expanded=False):
            st.json(meta)

    if truncated:
        with st.expander("Show full output"):
            full_text = extract_agent_text(result)
            st.code(full_text, language="text")


# --- MCP client lifecycle helpers ---

def append_log(msg: str):
    if "mcp_logs" not in st.session_state:
        st.session_state.mcp_logs = []
    st.session_state.mcp_logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}")


def start_kite_client(api_key: str, retries: int = 3, startup_timeout: int = 20) -> bool:
    """Start the MCP client and create the Agent. Store them in session_state."""
    if st.session_state.get("kite_client") is not None and st.session_state.get("agent") is not None:
        append_log("Kite client already running")
        return True

    # build model
    model = OpenAIModel(
        client_args={"api_key": api_key},
        model_id="gpt-4o",
        params={"max_tokens": 1000, "temperature": 0.7},
    )

    for attempt in range(1, retries + 1):
        append_log(f"Attempt {attempt} to start kite MCP client (timeout={startup_timeout}s)")
        try:
            kite_mcp_client = MCPClient(create_kite_transport)
            # Some MCPClient versions accept a timeout param on start(); try both ways
            try:
                kite_mcp_client.start(timeout=startup_timeout)
            except TypeError:
                kite_mcp_client.start()

            tools = kite_mcp_client.list_tools_sync()
            agent = Agent(model=model, tools=tools)

            st.session_state.kite_client = kite_mcp_client
            st.session_state.agent = agent
            append_log("MCP client started and Agent created successfully")
            return True
        except Exception as e:
            append_log(f"Start failed: {e}")
            append_log(traceback.format_exc())
            time.sleep(3)
            startup_timeout *= 2

    return False


def stop_kite_client():
    try:
        if st.session_state.get("kite_client"):
            st.session_state.kite_client.stop()
            st.session_state.kite_client = None
            st.session_state.agent = None
            append_log("MCP client stopped")
    except Exception as e:
        append_log(f"Error stopping client: {e}")
        append_log(traceback.format_exc())


# --- Streamlit UI ---

st.set_page_config(page_title="Kite MCP Agent", layout="centered")
st.title("Kite MCP Agent (Streamlit)")

# Sidebar: OpenAI API key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
#region = st.sidebar.text_input("AWS Region (optional)", value="ap-south-1")

if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to continue.")
    st.stop()

# initialize session placeholders
if "mcp_logs" not in st.session_state:
    st.session_state.mcp_logs = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "kite_client" not in st.session_state:
    st.session_state.kite_client = None
if "agent" not in st.session_state:
    st.session_state.agent = None

# Start the kite client (keeps it alive in session state). Show errors if can't start.
if st.session_state.kite_client is None:
    ok = start_kite_client(api_key=api_key, retries=3, startup_timeout=10)
    if not ok:
        st.error("Failed to start kite MCP client. See logs for details.")
        with st.expander("MCP logs (diagnostic)"):
            st.text_area("logs", "\n".join(st.session_state.mcp_logs[-200:]), height=300)
        st.stop()
    else:
        # request login link once and show to user
        try:
            login_response = st.session_state.agent("Give me link to login Zerodha Kite.")
            login_text = extract_agent_text(login_response)
            st.info(f"🔗 Please login here: {login_text}")
            append_log(f"Login response fetched: {login_text}")
        except Exception as e:
            append_log(f"Error retrieving login link: {e}")
            append_log(traceback.format_exc())
            st.error("Error requesting login link. Check logs.")
            with st.expander("MCP logs (diagnostic)"):
                st.text_area("logs", "\n".join(st.session_state.mcp_logs[-200:]), height=300)
            st.stop()

# Display logs expander
with st.expander("MCP logs (diagnostic)", expanded=False):
    st.text_area("logs", "\n".join(st.session_state.mcp_logs[-400:]), height=300)

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input
if user_query := st.chat_input("Ask question about your portfolio (or 'q' to quit)"):
    if user_query.lower().strip() == "q":
        st.session_state.messages.append({"role": "assistant", "content": "Goodbye 👋"})
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        try:
            response = st.session_state.agent(user_query)
            # Render in UI
            render_agent_result(response)
            # Store plain extracted text for history
            plain = extract_agent_text(response)
            st.session_state.messages.append({"role": "assistant", "content": plain})
        except Exception as e:
            append_log(f"Agent call failed: {e}")
            append_log(traceback.format_exc())
            err = f"Agent call failed: {e}"
            st.session_state.messages.append({"role": "assistant", "content": err})

# Controls
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Stop MCP client"):
        stop_kite_client()
        st.experimental_rerun()
with col2:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# Footer
st.caption("Kite MCP Agent — keep MCP client running in session state. Use the diagnostics panel if anything fails.")
