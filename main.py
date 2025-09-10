"""
LM Studio Chat - Streamlit Web Application
Simple chat interface for communicating with LM Studio.
"""
import streamlit as st
import uuid
from lm_studio_client import LMStudioClient


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'client' not in st.session_state:
        st.session_state.client = LMStudioClient()
    
    if 'connection_status' not in st.session_state:
        st.session_state.connection_status = None


def check_connection():
    """Check connection to LM Studio and display status."""
    if st.sidebar.button("Test Connection"):
        with st.spinner("Testing connection to LM Studio..."):
            result = st.session_state.client.test_connection()
            st.session_state.connection_status = result
    
    if st.session_state.connection_status:
        status = st.session_state.connection_status
        if status['status'] == 'success':
            st.sidebar.success(f"✅ {status['message']}")
            if 'models' in status:
                models = status['models'].get('data', [])
                if models:
                    st.sidebar.write(f"Available models: {len(models)}")
        else:
            st.sidebar.error(f"❌ {status['message']}")


def display_chat_messages():
    """Display chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    """Handle user input and get response from LM Studio."""
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from LM Studio
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare messages for API call
                api_messages = [{"role": msg["role"], "content": msg["content"]} 
                              for msg in st.session_state.messages]
                
                # Send request to LM Studio
                response = st.session_state.client.send_message(api_messages)
                
                # Extract and display response
                assistant_response = st.session_state.client.extract_message_content(response)
                st.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_response
                })


def sidebar_settings():
    """Display sidebar with settings and controls."""
    st.sidebar.title("Settings")
    
    # Connection section
    st.sidebar.subheader("Connection")
    check_connection()
    
    # Chat controls
    st.sidebar.subheader("Chat Controls")
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Server info
    st.sidebar.subheader("Server Info")
    st.sidebar.text(f"Host: {st.session_state.client.host}")
    st.sidebar.text(f"Port: {st.session_state.client.port}")
    
    # Statistics
    st.sidebar.subheader("Statistics")
    st.sidebar.text(f"Messages: {len(st.session_state.messages)}")


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="LM Studio Chat",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("💬 LM Studio Chat")
    st.markdown("Chat with your local LM Studio instance")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    sidebar_settings()
    
    # Main chat area
    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    main()
