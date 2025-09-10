# Návrh riešenia - LM Studio Chat Web App

## Analýza zadania

**Cieľ:** Vytvoriť jednoduchú web aplikáciu používajúcu Python Streamlit, ktorá umožní užívateľom chatovať s LM Studio serverom bežiacim na `193.168.1.123:1234`.

## Technické požiadavky

### Backend komunikácia
- **LM Studio API**: Komunikácia cez HTTP requests na `193.168.1.123:1234`
- **Protokol**: Pravdepodobne REST API alebo OpenAI-compatible API
- **Formát**: JSON požiadavky/odpovede

### Frontend (Streamlit)
- **Chat rozhranie**: Interaktívny chat s históriou
- **Input pole**: Pre zadávanie správ užívateľom
- **Zobrazenie odpovedí**: Formátované zobrazenie odpovede od LM Studio

## Architektúra riešenia

### Komponenty aplikácie
1. **Chat Interface** (Streamlit UI)
   - Input box pre správy
   - Chat história
   - Status indikátory (loading, error)

2. **API Client** (Python modul)
   - HTTP komunikácia s LM Studio
   - Spracovanie požiadaviek/odpovedí
   - Error handling

3. **Session Management** (Streamlit session state)
   - Udržiavanie chat histórie
   - Správa stavu konverzácie

### Dátový tok
```
Užívateľ → Streamlit UI → API Client → LM Studio → API Client → Streamlit UI → Užívateľ
```

## Implementačné detaily

### Potrebné knižnice
- `streamlit` - web framework
- `requests` - HTTP komunikácia
- `json` - spracovanie JSON dát

### Štruktúra projektu
```
lms_chatCC/
├── main.py              # Hlavná Streamlit aplikácia
├── lm_studio_client.py  # API client pre LM Studio
├── utils.py             # Pomocné funkcie
├── requirements.txt     # Závislosti
└── static/             # Statické súbory
```

### Konfigurácia
- Server URL: `193.168.1.123:1234`
- Configurable cez environment variables alebo config file
- Timeouts a retry logika

## Bezpečnostné aspekty
- Input validácia užívateľských správ
- Rate limiting (ak potrebné)
- Error handling pre sieťové chyby
- Žiadne logovanie citlivých dát

## Testovanie
- Testovanie pripojenia k LM Studio
- UI testovanie základných funkcionalít
- Error handling scenáre