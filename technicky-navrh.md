# Technický návrh - LM Studio Chat Interface

## API Komunikácia s LM Studio

### Endpoint Detection
LM Studio typicky poskytuje OpenAI-compatible API na týchto endpointoch:
- `POST /v1/chat/completions` - pre chat completion
- `GET /v1/models` - zoznam dostupných modelov

### Request Format
```json
{
  "model": "local-model", 
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
```

### Response Format
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      }
    }
  ]
}
```

## Streamlit UI Komponenty

### Layout
```python
# Header
st.title("LM Studio Chat")

# Chat container
chat_container = st.container()

# Input area
user_input = st.text_input("Type your message...")
send_button = st.button("Send")

# Sidebar (optional)
# - Model selection
# - Settings (temperature, max_tokens)
```

### Session State Management
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
```

## Error Handling Strategy

### Connection Errors
- Zobrazenie užívateľsky prívetivých chybových hlášok
- Retry mechanizmus s exponential backoff
- Fallback správanie pri nedostupnosti servera

### API Errors
- HTTP status code handling
- JSON parsing errors
- Timeout handling

### UI Error States
```python
try:
    response = lm_studio_client.send_message(message)
    st.success("Message sent successfully")
except ConnectionError:
    st.error("Cannot connect to LM Studio server")
except TimeoutError:
    st.error("Request timed out")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
```

## Performance Considerations

### Streaming Response (ak LM Studio podporuje)
```python
# Streamovanie odpovede pre lepší UX
response_placeholder = st.empty()
full_response = ""

for chunk in lm_studio_client.stream_response(message):
    full_response += chunk
    response_placeholder.write(full_response)
```

### Caching
```python
@st.cache_data
def get_available_models():
    return lm_studio_client.get_models()
```

## Konfigurácia

### Environment Variables
```
LM_STUDIO_HOST=193.168.1.123
LM_STUDIO_PORT=1234
LM_STUDIO_TIMEOUT=30
MAX_MESSAGE_LENGTH=1000
```

### Config File (optional)
```yaml
# config.yaml
lm_studio:
  host: "193.168.1.123"
  port: 1234
  timeout: 30
  
ui:
  page_title: "LM Studio Chat"
  max_message_length: 1000
```

## Development Workflow

### Running the Application
```bash
# Inštalácia závislostí
pip install -r requirements.txt

# Spustenie aplikácie
streamlit run main.py

# Development mode s auto-reload
streamlit run main.py --server.runOnSave true
```

### Testing
```bash
# Test connection to LM Studio
python -c "import lm_studio_client; print(lm_studio_client.test_connection())"

# Run basic functionality tests
python -m pytest tests/
```