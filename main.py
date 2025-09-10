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
    
    if 'available_models' not in st.session_state:
        st.session_state.available_models = []
        
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None


def check_connection():
    """Check connection to LM Studio and display status."""
    if st.sidebar.button("Test Connection"):
        with st.spinner("Testing connection to LM Studio..."):
            result = st.session_state.client.test_connection()
            st.session_state.connection_status = result
            
            # Update available models if connection is successful
            if result['status'] == 'success' and 'models' in result:
                models_data = result['models'].get('data', [])
                st.session_state.available_models = models_data
                
                # Set default model if none selected and models are available
                if not st.session_state.selected_model and models_data:
                    st.session_state.selected_model = models_data[0].get('id', 'local-model')
    
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
                
                # Send request to LM Studio with selected model
                response = st.session_state.client.send_message(
                    api_messages,
                    model=st.session_state.selected_model
                )
                
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
    
    # Model selection
    st.sidebar.subheader("Model Selection")
    if st.session_state.available_models:
        model_options = [model.get('id', 'Unknown') for model in st.session_state.available_models]
        
        # Find current selection index
        current_index = 0
        if st.session_state.selected_model:
            try:
                current_index = model_options.index(st.session_state.selected_model)
            except ValueError:
                current_index = 0
        
        selected_model = st.sidebar.selectbox(
            "Choose model:",
            options=model_options,
            index=current_index,
            help="Select which model to use for chat"
        )
        
        # Update selected model if changed
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.sidebar.success(f"Model changed to: {selected_model}")
    else:
        st.sidebar.info("📡 Connect first to load available models")
        if st.session_state.selected_model:
            st.sidebar.text(f"Using: {st.session_state.selected_model}")
    
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
    if st.session_state.selected_model:
        st.sidebar.text(f"Model: {st.session_state.selected_model}")


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
