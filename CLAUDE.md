# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python web application project called "lms-chatcc" that creates a Streamlit-based chat interface for LM Studio. The application connects to an LM Studio instance running on 193.168.1.123:1234 to enable user interaction with the language model.

## Development Setup

- **Python Version**: 3.13 (specified in `.python-version`)
- **Package Manager**: Uses `pyproject.toml` for dependency management
- **Main Entry Point**: `main.py` contains the basic application structure

## Common Commands

Since this is a Python project using `pyproject.toml` and uv:

```bash
# Install dependencies using uv
uv sync

# Run the Streamlit application
uv run streamlit run main.py

# Test LM Studio connection
uv run python lm_studio_client.py

# Run application in development mode
uv run streamlit run main.py --server.runOnSave true
```

## Architecture Notes

- **Streamlit Web Application**: Complete chat interface implemented
- **LM Studio Client**: HTTP communication module (`lm_studio_client.py`)
- **Session Management**: Chat history maintained in Streamlit session state
- **Error Handling**: Graceful handling of connection and API errors
- **Configuration**: Environment variables support for server settings
- Static assets stored in `static/` directory

## Project Structure

```
lms_chatCC/
├── main.py              # Streamlit chat application
├── lm_studio_client.py  # LM Studio API client
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── static/             # Static assets
```

## Key Features Implemented

- **Chat Interface**: Interactive chat with message history
- **Connection Testing**: Real-time connection status to LM Studio
- **Error Handling**: User-friendly error messages
- **Settings Sidebar**: Connection info, chat controls, statistics
- **Session Persistence**: Chat history maintained during session

The application connects to LM Studio at IP 192.168.1.123:1234 and provides a complete chat interface for user interaction.