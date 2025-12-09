import requests
import json
import os

try:
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
except (ImportError, FileNotFoundError, KeyError, AttributeError):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"

def get_client():
    """Returns a simple dict config for OpenRouter"""
    return {
        "api_key": OPENROUTER_API_KEY,
        "model": OPENROUTER_MODEL,
        "url": "https://openrouter.ai/api/v1/chat/completions"
    }

def send_chat_stream(messages: list, client_config: dict):
    """Send chat request to OpenRouter and yield response chunks"""
    try:
        response = requests.post(
            url=client_config["url"],
            headers={
                "Authorization": f"Bearer {client_config['api_key']}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://mediguider.streamlit.app",
                "X-Title": "MediGuideAI"
            },
            json={
                "model": client_config["model"],
                "messages": messages,
                "max_tokens": 1000
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            yield content
        else:
            yield f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        yield f"Error: {str(e)}"
