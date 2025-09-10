# Implementačný plán - LM Studio Chat App

## Fáza 1: Základná štruktúra (30 minút) ✅ DOKONČENÉ

### 1.1 Nastavenie projektu
- [x] Aktualizácia `pyproject.toml` so všetkými potrebnými závislosťami
- [x] Vytvorenie `requirements.txt` pre jednoduchšiu inštaláciu
- [x] Základná štruktúra súborov

### 1.2 Základný LM Studio client
- [x] Vytvorenie `lm_studio_client.py`
- [x] Implementácia základnej HTTP komunikácie
- [x] Test connection funkcia
- [x] Error handling pre network errors

## Fáza 2: Core funkcionalita (45 minút) ✅ DOKONČENÉ

### 2.1 API komunikácia
- [x] Implementácia chat completion endpoint
- [x] JSON request/response handling  
- [x] Model selection (automatická detekcia)
- [x] Konfigurácia (temperature, max_tokens)

### 2.2 Základné Streamlit UI
- [x] Prepísanie `main.py` na Streamlit aplikáciu
- [x] Chat input/output komponenty
- [x] Session state pre chat históriu
- [x] Základný styling a layout

## Fáza 3: Používateľské rozhranie (30 minút) ✅ DOKONČENÉ

### 3.1 Chat interface
- [x] Zobrazenie chat histórie (user/assistant messages)
- [x] Input validácia pomocou Streamlit
- [x] Loading states a progress indikátory
- [x] Clear chat funkcionalita

### 3.2 UI vylepšenia
- [x] Message formatting (markdown support)
- [x] Chat message komponenty
- [x] Auto-scroll pre nové správy
- [x] Responsive dizajn

## Fáza 4: Error handling a robustnosť (15 minút) ✅ DOKONČENÉ

### 4.1 Error states
- [x] Connection error handling
- [x] API error messages
- [x] Timeout handling
- [x] User-friendly error messages

### 4.2 Konfigurácia a nastavenia
- [x] Environment variables support
- [x] Configurable server URL
- [x] Sidebar s nastaveniami a štatistikami

## Fáza 5: Testovanie a finalizácia (15 minút) ✅ DOKONČENÉ

### 5.1 Testovanie
- [x] Test pripojenia k LM Studio serveru
- [x] Test základných Streamlit funkcionalít
- [x] Error scenarios testing
- [x] UI testing - aplikácia úspešne beží na porte 8502

### 5.2 Dokumentácia
- [x] Aktualizácia CLAUDE.md s usage instructions
- [x] Komentáre v kóde
- [x] Implementačný plán dokončený

## Súbory na vytvorenie/úpravu

### Nové súbory
1. `lm_studio_client.py` - API client pre LM Studio
2. `requirements.txt` - Python dependencies  
3. `config.py` - Konfiguračné nastavenia (optional)

### Súbory na úpravu
1. `main.py` - Prepísanie na Streamlit aplikáciu
2. `pyproject.toml` - Pridanie dependencies
3. `README.md` - Dokumentácia používania

## Dependencies potrebné v pyproject.toml

```toml
dependencies = [
    "streamlit>=1.28.0",
    "requests>=2.31.0",
    "python-dotenv>=1.0.0"
]
```

## Kritické rozhodnutia

1. **API Format**: Predpokladáme OpenAI-compatible API
2. **State Management**: Použitie Streamlit session state
3. **Error Handling**: Graceful degradation s user-friendly messages
4. **Configuration**: Environment variables + optional config file

## Potenciálne problémy a riešenia

1. **CORS Issues**: LM Studio môže mať CORS restrictions
   - Riešenie: Proxy requests cez backend ak potrebné

2. **Streaming**: LM Studio nemusí podporovať streaming
   - Riešenie: Fallback na regular requests

3. **Authentication**: LM Studio môže vyžadovať auth
   - Riešenie: Konfigurovateľné API keys

4. **Model Selection**: Nemusí byť dostupné cez API
   - Riešenie: Hardcoded model name alebo manual config