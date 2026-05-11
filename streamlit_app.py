import streamlit as st
from st_chat_message import message

from src.portfolioagent import PortfolioAgent

# Page config
st.set_page_config(page_title="Portfolio AI Agent")

st.title("📈 Portfolio AI Agent")

# Initialize agent once
if "agent" not in st.session_state:
    st.session_state.agent = PortfolioAgent()

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Ask about your portfolio...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Call your agent
    response = st.session_state.agent.answer_question(
        question=user_input
    )

    # Extract response text
    bot_reply = response.text

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # Save metadata separately
    st.session_state.last_usage = response.usage_metadata
    st.session_state.last_tool_history = response.automatic_function_calling_history

# Display chat messages
for msg in st.session_state.messages:

    if msg["role"] == "user":
        message(msg["content"], is_user=True)

    else:
        message(msg["content"], is_user=False)

# Optional Debug Section
if "last_usage" in st.session_state:

    with st.expander("📊 Token Usage"):

        usage = st.session_state.last_usage

        st.write("Prompt Tokens:", usage.prompt_token_count)
        st.write("Completion Tokens:", usage.candidates_token_count)
        st.write("Total Tokens:", usage.total_token_count)

# Optional Tool Calls Section
if "last_tool_history" in st.session_state:

    with st.expander("🛠 Tool Calls"):

        history = st.session_state.last_tool_history

        for item in history:

            if item.role == "model":

                for part in item.parts:

                    if hasattr(part, "function_call") and part.function_call:

                        st.markdown("### Tool Used")
                        st.write("Function:", part.function_call.name)
                        st.json(part.function_call.args)

            elif item.role == "user":

                for part in item.parts:

                    if hasattr(part, "function_response") and part.function_response:

                        st.markdown("### Tool Response")
                        st.write(part.function_response.response)