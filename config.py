import os
import openai
from typing import Dict, Generator
import streamlit as st

def get_client() -> Dict:
    """Get OpenRouter client configuration with proper error handling"""
    api_key = ""
    
    # Priority 1: Try Streamlit secrets (for cloud deployment)
    try:
        if hasattr(st, 'secrets') and 'OPENROUTER_API_KEY' in st.secrets:
            api_key = st.secrets["OPENROUTER_API_KEY"]
            st.sidebar.success("✓ Using API key from Streamlit secrets")
    except Exception as e:
        st.sidebar.warning(f"Could not read Streamlit secrets: {e}")
    
    # Priority 2: Try environment variable (for local development)
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if api_key:
            st.sidebar.info("✓ Using API key from environment variable")
    
    # Priority 3: Check for placeholder
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        st.sidebar.error("❌ API key not configured")
        return {
            "api_key": "",
            "base_url": "https://openrouter.ai/api/v1",
            "model": "anthropic/claude-3.5-sonnet",
            "headers": {}
        }
    
    return {
        "api_key": api_key,
        "base_url": "https://openrouter.ai/api/v1",
        "model": "anthropic/claude-3.5-sonnet",
        "headers": {
            "HTTP-Referer": "https://mediguideai.streamlit.app",
            "X-Title": "MediGuideAI"
        }
    }

def send_chat_stream(messages, client_config=None, **kwargs) -> Generator[str, None, None]:
    """Send chat stream with better error handling"""
    if not client_config:
        client_config = get_client()
    
    api_key = client_config.get("api_key", "")
    
    # Check if API key is missing or placeholder
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        yield "🔑 **API Key Required**\n\n"
        yield "To use the AI Chat feature, you need to:\n"
        yield "1. Get an API key from [OpenRouter](https://openrouter.ai/keys)\n"
        yield "2. Add it to Streamlit Cloud secrets (.streamlit/secrets.toml)\n\n"
        yield "**For now, this is a demo with sample responses.**\n"
        yield "\nHere's what I would say about your query:\n"
        yield "Sleep disorders can include insomnia, sleep apnea, restless legs syndrome, and narcolepsy. "
        yield "Common symptoms include difficulty falling asleep, frequent awakenings, daytime fatigue, and snoring. "
        yield "For proper diagnosis and treatment, consult a sleep specialist or healthcare provider."
        return
    
    try:
        # Initialize OpenAI client with OpenRouter
        client = openai.OpenAI(
            api_key=api_key,
            base_url=client_config.get("base_url", "https://openrouter.ai/api/v1")
        )
        
        # Make API call
        response = client.chat.completions.create(
            model=client_config.get("model", "anthropic/claude-3.5-sonnet"),
            messages=messages,
            stream=True,
            **kwargs
        )
        
        # Stream the response
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except openai.AuthenticationError as e:
        yield f"❌ **Authentication Error (401):**\n\n"
        yield "Your API key is invalid or expired.\n\n"
        yield "**Please check:**\n"
        yield "1. Is your OpenRouter API key correct?\n"
        yield "2. Has it expired?\n"
        yield "3. Do you have sufficient credits?\n\n"
        yield "Get a new key from: https://openrouter.ai/keys"
        
    except openai.APIError as e:
        yield f"❌ **API Error:**\n\n"
        yield f"{str(e)}\n\n"
        yield "Please try again or check your OpenRouter account."
        
    except Exception as e:
        yield f"❌ **Error:** {str(e)}\n\n"
        yield "Please try again later or contact support."
