# Whatsapp_Chatbot_using_API

A WhatsApp chatbot that uses **ThingESP** for messaging and **Google Gemini** for AI responses.

## Features
- Receives WhatsApp queries via ThingESP
- Generates AI responses using Gemini
- Replies automatically through MQTT

## Requirements
- Python 3.8+
- ThingESP account credentials
- Google Gemini API key

## Installation
```bash
pip install google-genai paho-mqtt
```

## Configuration
Edit these values inside `WhatsChatbot.py`:

```python
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")
thing = Client('YOUR_USERNAME', 'YOUR_PROJECT_NAME', 'YOUR_PASSWORD')
```

## Usage
Run the script:

```bash
python WhatsChatbot.py
```

Your bot will listen for incoming messages and respond automatically.

## Notes
- Keep your API keys secret.
- You can customize `handleResponse()` to modify how replies are generated.

## License
MIT (or your preferred license)
