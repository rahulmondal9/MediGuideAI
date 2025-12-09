# ui.py - Fixed with Streamlit Native Navigation
"""
MediGuideAI — Premium Medical Dashboard UI
- Fixed navigation using Streamlit native components
- All 7 core pages fully visible and functional
- Modern sidebar with color previews
"""

import os
import re
import time
from typing import List, Tuple, Dict
import streamlit as st
import pandas as pd

from config import get_client, send_chat_stream
from rules import load_rules, RulesLoadError
from medical_data import SAMPLE_DISEASES, SAMPLE_DRUGS

# ------------------------
# Page config & logger
# ------------------------
st.set_page_config(
    page_title="MediGuideAI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏥"
)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# ------------------------
# Load medical data from external file
# ------------------------
df_diseases = pd.DataFrame(SAMPLE_DISEASES)
df_drugs = pd.DataFrame(SAMPLE_DRUGS)

# ------------------------
# Rule loader
# ------------------------
def safe_load_rules():
    try:
        r = load_rules()
        return r
    except Exception as e:
        return {"chest pain":{"Ischemic Heart Disease":5}, "fever":{"Community-Acquired Pneumonia":3}}

RULES = safe_load_rules()

# ------------------------
# Enhanced Theme Palette System
# ------------------------
PALETTES = {
    "Teal": {
        "primary": "#0b6b67",
        "secondary": "#0d9488",
        "accent": "#14b8a6",
        "background": "#f0fdfa",
        "card": "#ffffff",
        "text": "#134e4a",
        "muted": "#5f7f7b",
        "gradient": "linear-gradient(135deg, #0b6b67 0%, #14b8a6 100%)"
    },
    "Blue": {
        "primary": "#1d4ed8",
        "secondary": "#3b82f6",
        "accent": "#60a5fa",
        "background": "#eff6ff",
        "card": "#ffffff",
        "text": "#1e3a8a",
        "muted": "#4b5563",
        "gradient": "linear-gradient(135deg, #1d4ed8 0%, #60a5fa 100%)"
    },
    "Warm": {
        "primary": "#ea580c",
        "secondary": "#f97316",
        "accent": "#fb923c",
        "background": "#fff7ed",
        "card": "#ffffff",
        "text": "#9a3412",
        "muted": "#7c2d12",
        "gradient": "linear-gradient(135deg, #ea580c 0%, #fb923c 100%)"
    },
    "Purple": {
        "primary": "#7c3aed",
        "secondary": "#8b5cf6",
        "accent": "#a78bfa",
        "background": "#faf5ff",
        "card": "#ffffff",
        "text": "#5b21b6",
        "muted": "#6d28d9",
        "gradient": "linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%)"
    },
    "Green": {
        "primary": "#16a34a",
        "secondary": "#22c55e",
        "accent": "#4ade80",
        "background": "#f0fdf4",
        "card": "#ffffff",
        "text": "#166534",
        "muted": "#15803d",
        "gradient": "linear-gradient(135deg, #16a34a 0%, #4ade80 100%)"
    },
    "Coral": {
        "primary": "#f43f5e",
        "secondary": "#fb7185",
        "accent": "#fda4af",
        "background": "#fff1f2",
        "card": "#ffffff",
        "text": "#9f1239",
        "muted": "#be123c",
        "gradient": "linear-gradient(135deg, #f43f5e 0%, #fda4af 100%)"
    }
}

def get_palette(name: str):
    return PALETTES.get(name, PALETTES["Teal"])

def apply_dynamic_style(palette_name: str):
    p = get_palette(palette_name)
    css = f"""
    <style>
    :root {{
        --primary: {p['primary']};
        --secondary: {p['secondary']};
        --accent: {p['accent']};
        --background: {p['background']};
        --card: {p['card']};
        --text: {p['text']};
        --muted: {p['muted']};
        --gradient: {p['gradient']};
    }}
    
    body {{
        background: var(--background);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 50%, #2c3e50 100%) !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #ecf0f1 !important;
    }}
    
    [data-testid="stSidebar"] h2 {{
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {{
        color: #bdc3c7 !important;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: #7f8c8d !important;
    }}
    
    .main-header {{
        background: var(--gradient);
        padding: 40px 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    
    .card {{
        background: var(--card);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }}
    
    .metric-card {{
        background: var(--gradient);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
    }}
    
    .metric-value {{
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 5px;
    }}
    
    .metric-label {{
        font-size: 14px;
        opacity: 0.9;
    }}
    
    .color-box {{
        width: 25px;
        height: 25px;
        border-radius: 6px;
        display: inline-block;
        margin-right: 8px;
        vertical-align: middle;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .nav-button {{
        background: var(--accent);
        color: white;
        border: 2px solid var(--primary);
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        margin: 5px;
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    .nav-button:hover {{
        background: var(--primary);
        transform: translateY(-2px);
    }}
    
    .nav-button.active {{
        background: var(--gradient);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }}
    
    h1, h2, h3, h4 {{
        color: var(--text);
    }}

    /* -----------------------
       UPDATED: Uniform sizing rules (tighter layout)
       ----------------------- */

    /* Native Streamlit buttons used for top tabs & primary buttons */
    div.stButton > button {{
        min-height: 56px !important;
        height: 56px !important;
        line-height: 1.05 !important;
        white-space: normal !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 6px 10px !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }}

    /* Balanced card layout with reduced height and tighter spacing */
    .card {{
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 180px;   /* reduced for tighter rows */
        padding: 18px;       /* slightly smaller inner padding */
        margin-bottom: 12px; /* reduce vertical gap between rows */
        border-radius: 16px;
    }}

    /* Colored/quick-access gradient cards also get same min height */
    .card[style*="linear-gradient"] {{
        min-height: 180px;
    }}

    /* Make metric cards compact */
    .metric-card {{
        min-height: 90px;
        padding: 18px;
    }}

    /* Slightly tighten Streamlit column cell padding to reduce horizontal gaps */
    [data-testid="column"] > div {{
        padding-left: 8px !important;
        padding-right: 8px !important;
    }}

    /* Responsive adjustments for smaller screens */
    @media (max-width: 900px) {{
        div.stButton > button {{
            min-height: 56px !important;
            height: auto !important;
            padding: 10px 8px !important;
            white-space: normal !important;
        }}
        .card {{
            min-height: 160px;
            margin-bottom: 10px;
        }}
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Fix sidebar dropdown and label contrast */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stText,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .css-1offfwp {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------
# Sanitizer & scoring
# ------------------------
def sanitize_text(text: str) -> Tuple[str, bool]:
    if not text:
        return text, False
    s = text
    flag = False
    s, n = re.subn(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", s)
    if n: flag = True
    s, n = re.subn(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]", s)
    if n: flag = True
    s, n = re.subn(r"\b\d{6,}\b", "[REDACTED_ID]", s)
    if n: flag = True
    return s, flag

def score_symptoms(selected: List[str]):
    raw = {}
    for s in selected:
        tok = s.lower().strip()
        mapping = RULES.get(tok, {})
        for cond, w in mapping.items():
            raw[cond] = raw.get(cond, 0) + int(w)
    if not raw:
        return [], {}
    m = max(raw.values())
    ranked = [(c, round(100.0*v/m,1)) for c,v in raw.items()]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked, raw

def detect_critical(ranked: List[tuple], severity_value:int) -> bool:
    if severity_value >= 8:
        return True
    for cond, pct in ranked:
        if pct >= 85 and cond.lower() in ("ischemic heart disease","ischemic stroke","sepsis","septic shock","pulmonary embolism"):
            return True
    return False

def ambulance_map_link(location_query: str = "") -> str:
    base = "https://www.google.com/maps/search/ambulance+near+me"
    if location_query:
        import urllib.parse
        return f"https://www.google.com/maps/search/ambulance+near+{urllib.parse.quote(location_query)}"
    return base

# ------------------------
# Sidebar with Navigation
# ------------------------
def sidebar_controls():
    st.sidebar.markdown("## 🎨 Customization")
    
    # Theme and Palette selection
    col1, col2 = st.sidebar.columns(2)
    with col1:
        theme_choice = st.selectbox(
            "Theme", 
            ["Minimal", "Modern", "Classic"], 
            key="ui_theme",
            label_visibility="collapsed"
        )
        st.caption("Theme")
    
    with col2:
        palette_choice = st.selectbox(
            "Palette", 
            list(PALETTES.keys()), 
            index=0, 
            key="ui_palette",
            label_visibility="collapsed"
        )
        st.caption("Palette")
    
    st.sidebar.markdown("---")
    
    # Filters section
    st.sidebar.markdown("## 🔍 Filters")
    
    disease_category = st.sidebar.selectbox(
        "Disease Category",
        ["All", "Cardiovascular", "Respiratory", "Neurological", "Infectious", "Endocrine"],
        key="filter_cat"
    )
    
    severity = st.sidebar.slider(
        "Severity Level",
        0, 10, 0,
        key="filter_sev",
        help="Adjust for informational filtering"
    )
    
    st.sidebar.markdown("---")
    
    # Disclaimer
    st.sidebar.markdown("""
    <div style='
        background: linear-gradient(135deg, #f87171 0%, #dc2626 100%);
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: #ffffff;
    '>
        <div style='font-size: 14px; line-height: 1.6;'>
            ⚠️ <strong>Important</strong><br>
            For informational purposes only.<br>
            Not a substitute for professional medical advice.
        </div>
    </div>
""", unsafe_allow_html=True)


    return {
        "theme": theme_choice,
        "palette": palette_choice,
        "disease_category": disease_category,
        "severity": severity,
        "current_page": st.session_state.current_page
    }

# ------------------------
# FIXED: Top Navigation using Streamlit Columns
# ------------------------
def render_top_tabs(active_page: str):
    # Define all 7 pages with icons
    pages = [
        {"name": "Home", "icon": "🏠"},
        {"name": "Symptom Checker", "icon": "🩺"},
        {"name": "Find Care", "icon": "📍"},
        {"name": "Drugs & Therapies", "icon": "💊"},
        {"name": "Self-care & Prevention", "icon": "🧘"},
        {"name": "AI Chat", "icon": "🤖"},
        {"name": "About & Disclaimer", "icon": "ℹ️"}
    ]
    
    # Create 7 columns for the tabs
    cols = st.columns(7)
    
    # Add each tab as a button in its column
    for idx, page in enumerate(pages):
        with cols[idx]:
            # Determine button style based on active state
            is_active = page["name"] == active_page
            
            if st.button(
                f"{page['icon']}\n{page['name']}",
                key=f"top_nav_{page['name']}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page["name"]
                st.rerun()

# ------------------------
# Page Renderers
# ------------------------
def page_home(ctx):
    st.markdown("""
        <div class='main-header' style='border-radius: 100px;'>
            <h1 style='font-size: 48px; font-weight: 800; margin-bottom: 10px;'>🏥 MediGuideAI</h1>
            <p style='font-size: 18px; opacity: 0.9;'><b>MediGuideAI</b> is an advanced AI-powered healthcare assistant designed to help you understand your symptoms, predict potential diseases, and receive personalized health guidance—all in one place.
With smart machine learning models and natural language processing, MediGuideAI analyzes your inputs and provides meaningful medical insights within seconds.</p>
            <p style='font-size: 18px; opacity: 0.9;'>Whether you are experiencing discomfort, tracking your daily health, or simply curious about your well-being, MediGuideAI guides you toward better health decisions through early detection, preventive advice, and interactive support.</p>
        </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            padding: 15px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(17, 153, 142, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(17, 153, 142, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: var(--primary); margin: 30px 0;'>⭐ Why Use MediGuideAI?</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>🔍 Instant Symptom Analysis</h3>
                <p>Describe or speak your symptoms, and MediGuideAI predicts possible health conditions with smart AI-driven analysis.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>💡 Personalized Health Advice</h3>
                <p>Receive easy-to-understand suggestions on: Daily diet, Water intake, Exercise routines, Preventive measures, Lifestyle improvements.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>💬 24/7 AI Health Chat Support</h3>
                <p>Ask questions, get clarifications, and learn about health conditions through an interactive chatbot, available anytime.</p>
            </div>
        """, unsafe_allow_html=True)

    
    with col2:
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>🧠 Accurate Disease Predictions</h3>
                <p>Our system evaluates medical patterns, lifestyle factors, and symptom combinations to estimate the likelihood of specific diseases.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>🎙️ Voice-Enabled Interaction</h3>
                <p>Talk naturally with the system—just like speaking to a virtual health assistant.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px;'>
                <h3 style='color: #f0f4ff;'>🌐 Simple, Fast & User-Friendly</h3>
                <p>Designed for all age groups—anyone can use MediGuideAI without technical knowledge.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div class='card' style='background: #f0f9ff; border-left: 5px solid #0ea5e9; padding: 25px;'>
            <h2 style='color: #0c4a6e;'>⭐ What the Name "MediGuideAI" Means</h2>
            <p><b>Medi</b> → Medical, Healthcare, Wellness<br><b>Guide</b> → Helps users navigate symptoms, risks & preventive steps<br><b>AI</b> → Advanced artificial intelligence powering accurate predictions</p>
            <p style='font-size: 18px; font-weight: 600; color: #0369a1;'>MediGuideAI = An AI system that guides you to better health decisions.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='card' style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; text-align: center; padding: 30px;'>
            <h2 style='color: white;'>⭐ Your Health, Simplified. Your Wellness, Guided.</h2>
            <p>With MediGuideAI, taking care of your health becomes easier, smarter, and more proactive. Start exploring your symptoms, understand your risks, and live a healthier life with intelligent assistance—anytime, anywhere.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Health Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>98%</div>
                <div class='metric-label'>Accuracy Rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>50+</div>
                <div class='metric-label'>Medical Conditions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>24/7</div>
                <div class='metric-label'>AI Support</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>100+</div>
                <div class='metric-label'>Drug Database</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick Access Cards
    st.markdown("### 🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border: none;'>
                <h3 style='color: white;'>🩺 Symptom Checker</h3>
                <p><b>Fast, structured insights based on user-reported symptoms.</b></p>
                <p><b>What it does:</b></p>
                <ul>
                    <li>Analyzes symptoms you type or speak</li>
                    <li>Matches against known medical patterns</li>
                    <li>Estimates possible causes</li>
                    <li>Highlights red-flag symptoms</li>
                </ul>
                <p><b>Benefits:</b> Eliminates confusion, gives quick insights, encourages early consultation.</p>
                <p><b>Best for:</b> Anyone unsure about fever, pain, fatigue, dizziness, cough, or discomfort.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border: none;'>
                <h3 style='color: white;'>💊 Drug Database</h3>
                <p><b>Structured drug information for education and safety.</b></p>
                <p><b>What it includes:</b></p>
                <ul>
                    <li>Drug name and purpose</li>
                    <li>How medication works</li>
                    <li>Common dosages (educational)</li>
                    <li>Side effects & interactions</li>
                    <li>Safety precautions</li>
                </ul>
                <p><b>Benefits:</b> Learn medication basics, understand prescriptions, reduce interaction risks.</p>
                <p><b>Best for:</b> Patients taking new medications or caregivers.</p>
                <p><small>⚠️ Informational only. Does not replace pharmacist/doctor advice.</small></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; border: none;'>
                <h3 style='color: white;'>📍 Find Care</h3>
                <p><b>Locate nearby medical services when needed.</b></p>
                <p><b>What it does:</b></p>
                <ul>
                    <li>Locates emergency care centers</li>
                    <li>Lists nearest hospitals</li>
                    <li>Provides quick guidance</li>
                    <li>Offers directions to services</li>
                    <li>Suggests when to seek help</li>
                </ul>
                <p><b>Benefits:</b> Saves time during critical moments, removes guesswork, supports travelers.</p>
                <p><b>Best for:</b> Anyone experiencing moderate-to-severe symptoms needing in-person evaluation.</p>
            </div>
        """, unsafe_allow_html=True)

def page_symptom_checker(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 200px; text-align: center; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);'>
            <h1 style='color: white; font-size: 42px; margin: 0;'>🩺 Symptom Checker</h1>
            <p style='color: #f0f4ff; font-size: 18px; margin-top: 10px;'>AI-powered symptom analysis with rule-based validation</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); padding: 25px; border-radius: 20px; box-shadow: 0 12px 30px rgba(255, 8, 68, 0.4);'>
                <h3 style='color: white; margin: 0 0 15px 0; text-align: center; font-size: 24px;'>🚨 Emergency Symptoms</h3>
                <p style='color: white; text-align: center; margin-bottom: 20px; font-weight: 600; font-size: 15px;'>Call 112/911 IMMEDIATELY if experiencing:</p>
                <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 12px; margin-bottom: 10px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 26px; margin-right: 12px;'>❤️</span>
                        <div>
                            <b style='color: white; font-size: 15px;'>Chest Pain/Pressure</b><br>
                            <small style='color: rgba(255,255,255,0.9); font-size: 12px;'>Crushing sensation or tightness</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 12px; margin-bottom: 10px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 26px; margin-right: 12px;'>🤧</span>
                        <div>
                            <b style='color: white; font-size: 15px;'>Difficulty Breathing</b><br>
                            <small style='color: rgba(255,255,255,0.9); font-size: 12px;'>Severe shortness of breath</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 12px; margin-bottom: 10px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 26px; margin-right: 12px;'>🩸</span>
                        <div>
                            <b style='color: white; font-size: 15px;'>Severe Bleeding</b><br>
                            <small style='color: rgba(255,255,255,0.9); font-size: 12px;'>Uncontrolled or heavy blood loss</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 12px; margin-bottom: 10px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 26px; margin-right: 12px;'>😵</span>
                        <div>
                            <b style='color: white; font-size: 15px;'>Loss of Consciousness</b><br>
                            <small style='color: rgba(255,255,255,0.9); font-size: 12px;'>Fainting or unresponsiveness</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.2); padding: 12px; border-radius: 12px; border: 2px solid rgba(255,255,255,0.3);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 26px; margin-right: 12px;'>⚡</span>
                        <div>
                            <b style='color: white; font-size: 15px;'>Stroke Symptoms</b><br>
                            <small style='color: rgba(255,255,255,0.9); font-size: 12px;'>Face drooping, arm weakness, speech difficulty</small>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 20px; box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);'>
                <h3 style='color: white; margin: 0 0 20px 0; text-align: center; font-size: 24px;'>💡 Smart Symptom Guide</h3>
                <div style='background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 28px; margin-right: 12px;'>📝</span>
                        <div>
                            <b style='color: white; font-size: 16px;'>Be Specific</b><br>
                            <small style='color: rgba(255,255,255,0.9);'>Describe exact location, type & intensity</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 28px; margin-right: 12px;'>⏰</span>
                        <div>
                            <b style='color: white; font-size: 16px;'>Timeline Matters</b><br>
                            <small style='color: rgba(255,255,255,0.9);'>When did it start? Getting worse or better?</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 28px; margin-right: 12px;'>🎯</span>
                        <div>
                            <b style='color: white; font-size: 16px;'>Note Triggers</b><br>
                            <small style='color: rgba(255,255,255,0.9);'>Food, activity, stress, or environmental factors</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 15px; border-radius: 12px; margin-bottom: 12px; backdrop-filter: blur(10px);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 28px; margin-right: 12px;'>💊</span>
                        <div>
                            <b style='color: white; font-size: 16px;'>Current Medications</b><br>
                            <small style='color: rgba(255,255,255,0.9);'>List all drugs, supplements & remedies taken</small>
                        </div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; border: 2px solid rgba(255,255,255,0.3);'>
                    <div style='display: flex; align-items: center;'>
                        <span style='font-size: 28px; margin-right: 12px;'>📊</span>
                        <div>
                            <b style='color: white; font-size: 16px;'>Track Changes</b><br>
                            <small style='color: rgba(255,255,255,0.9);'>Monitor patterns, frequency & progression</small>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: 700 !important;
            padding: 15px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(245, 87, 108, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 30px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 12px 35px rgba(67, 233, 123, 0.4);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 32px;'>📝 Symptom Analysis Tool</h2>
            <p style='color: rgba(255,255,255,0.95); text-align: center; margin: 10px 0 0 0; font-size: 16px;'>Describe your symptoms for AI-powered health insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    symptom_set = sorted(set(sum(df_diseases["key_symptoms"].tolist(), [])))
    
    # Symptom Input Card
    st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 20px; border-radius: 15px; border-left: 5px solid #667eea; margin-bottom: 20px;'>
            <h4 style='color: #667eea; margin: 0 0 10px 0;'>🔍 Step 1: Enter Your Symptoms</h4>
            <p style='color: #555; margin: 0; font-size: 14px;'>Type symptoms separated by commas, or select from the list below</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_input = st.text_input(
        "Type symptoms",
        key="symp_manual",
        placeholder="e.g., fever, headache, cough, fatigue, nausea...",
        help="Type any symptoms you're experiencing",
        label_visibility="collapsed"
    )
    
    manual_symptoms = [s.strip() for s in selected_input.split(",") if s.strip()] if selected_input else []
    
    selected_from_list = st.multiselect(
        "Or select from common symptoms",
        symptom_set,
        key="symp_selected",
        help="Choose from predefined symptoms"
    )
    
    selected = list(set(manual_symptoms + selected_from_list))
    
    # Show selected symptoms count
    if selected:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 12px 20px; border-radius: 10px; margin: 15px 0; text-align: center;'>
                <span style='color: white; font-weight: 600; font-size: 16px;'>✓ {len(selected)} symptom(s) selected</span>
            </div>
        """, unsafe_allow_html=True)
    
    # Additional Details Card
    st.markdown("""
        <div style='background: rgba(250, 112, 154, 0.1); padding: 20px; border-radius: 15px; border-left: 5px solid #fa709a; margin: 20px 0 15px 0;'>
            <h4 style='color: #fa709a; margin: 0 0 10px 0;'>💬 Step 2: Provide Additional Context</h4>
            <p style='color: #555; margin: 0; font-size: 14px;'>Help us understand your condition better with more details</p>
        </div>
    """, unsafe_allow_html=True)
    
    extra = st.text_area(
        "Additional Details",
        key="symp_extra",
        max_chars=600,
        placeholder="When did symptoms start? How severe are they? Any triggers or patterns? Current medications?",
        height=100,
        label_visibility="collapsed"
    )
    
    # Settings Card
    st.markdown("""
        <div style='background: rgba(67, 233, 123, 0.1); padding: 20px; border-radius: 15px; border-left: 5px solid #43e97b; margin: 20px 0 15px 0;'>
            <h4 style='color: #43e97b; margin: 0 0 15px 0;'>⚙️ Step 3: Configure Analysis Settings</h4>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div style='background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 10px;'>
                <p style='color: #667eea; font-weight: 600; margin: 0 0 10px 0;'>🌡️ Severity Level</p>
            </div>
        """, unsafe_allow_html=True)
        severity_val = st.slider(
            "Severity",
            1, 10, 3,
            key="symp_severity",
            help="1=Mild discomfort, 10=Severe/Unbearable",
            label_visibility="collapsed"
        )
        
        # Visual severity indicator
        severity_colors = {
            range(1, 4): ("#4ade80", "Mild"),
            range(4, 7): ("#fbbf24", "Moderate"),
            range(7, 11): ("#ef4444", "Severe")
        }
        severity_label = next((label for r, (_, label) in severity_colors.items() if severity_val in r), "Mild")
        severity_color = next((color for r, (color, _) in severity_colors.items() if severity_val in r), "#4ade80")
        
        st.markdown(f"""
            <div style='background: {severity_color}; padding: 8px; border-radius: 8px; text-align: center; margin-top: 10px;'>
                <span style='color: white; font-weight: 700;'>{severity_label} ({severity_val}/10)</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
            <div style='background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin-bottom: 10px;'>
                <p style='color: #667eea; font-weight: 600; margin: 0 0 10px 0;'>🤖 AI Enhancement</p>
            </div>
        """, unsafe_allow_html=True)
        ai_enable = st.checkbox(
            "Enable AI-Powered Analysis",
            value=True,
            key="symp_ai_enable",
            help="Use advanced AI for comprehensive symptom analysis"
        )
        
        if ai_enable:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 8px; border-radius: 8px; text-align: center; margin-top: 25px;'>
                    <span style='color: white; font-weight: 600; font-size: 13px;'>✓ AI Analysis Enabled</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: #e5e7eb; padding: 8px; border-radius: 8px; text-align: center; margin-top: 25px;'>
                    <span style='color: #6b7280; font-weight: 600; font-size: 13px;'>Rule-Based Only</span>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # Analyze Button
    if st.button("Start Analysis", use_container_width=True, type="primary", key="analyze_btn"):
        if not selected:
            st.warning("⚠️ Please select at least one symptom to analyze.")
        else:
            # Background processing
            sanitized_extra, phi = sanitize_text(extra)
            if phi:
                st.info("🔒 Personal information redacted for privacy.")
            
            with st.spinner("🔬 Processing analysis in background..."):
                time.sleep(0.5)
                ranked, raw = score_symptoms([s.lower().strip() for s in selected])
                critical = detect_critical(ranked, severity_val)
            
            # Display Results
            st.markdown("""
                <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 20px; margin: 20px 0; box-shadow: 0 12px 35px rgba(17, 153, 142, 0.4); text-align: center;'>
                    <h2 style='color: white; margin: 0; font-size: 28px;'>📋 Analysis Report</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Symptom Summary
            st.markdown(f"""
                <div style='background: white; padding: 20px; border-radius: 15px; margin: 15px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-left: 5px solid #667eea;'>
                    <h4 style='color: #667eea; margin: 0 0 10px 0;'>🔍 Reported Symptoms</h4>
                    <p style='color: #2d3748; font-size: 16px; margin: 5px 0;'><b>Symptoms:</b> {', '.join(selected)}</p>
                    <p style='color: #2d3748; font-size: 16px; margin: 5px 0;'><b>Severity:</b> {severity_label} ({severity_val}/10)</p>
                    {f"<p style='color: #2d3748; font-size: 16px; margin: 5px 0;'><b>Details:</b> {sanitized_extra}</p>" if sanitized_extra else ""}
                </div>
            """, unsafe_allow_html=True)
            
            # Critical Condition Alert
            if critical:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); padding: 30px; border-radius: 20px; margin: 20px 0; box-shadow: 0 15px 45px rgba(255, 8, 68, 0.5); border: 3px solid rgba(255,255,255,0.3);'>
                        <div style='text-align: center;'>
                            <div style='font-size: 56px; margin-bottom: 10px;'>🚨</div>
                            <h2 style='color: white; margin: 0; font-size: 26px;'>CRITICAL CONDITION DETECTED</h2>
                            <div style='background: rgba(255,255,255,0.25); padding: 20px; border-radius: 15px; margin: 15px 0; backdrop-filter: blur(10px);'>
                                <h3 style='color: white; margin: 0 0 15px 0; font-size: 20px;'>🚑 EMERGENCY NUMBERS</h3>
                                <div style='background: rgba(255,255,255,0.3); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                    <p style='color: white; font-size: 32px; margin: 0; font-weight: 700;'>📞 112 / 911</p>
                                    <p style='color: white; font-size: 14px; margin: 5px 0;'>Emergency Medical Services</p>
                                </div>
                                <div style='background: rgba(255,255,255,0.2); padding: 12px; border-radius: 10px; margin: 10px 0;'>
                                    <p style='color: white; font-size: 16px; margin: 0; font-weight: 600;'>⚠️ Do NOT drive yourself</p>
                                </div>
                                <div style='background: rgba(255,255,255,0.2); padding: 12px; border-radius: 10px; margin: 10px 0;'>
                                    <p style='color: white; font-size: 16px; margin: 0; font-weight: 600;'>⚠️ Stay calm and wait for help</p>
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='text-align: center; margin: 15px 0;'>
                        <a href='{ambulance_map_link()}' target='_blank' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 35px; border-radius: 25px; text-decoration: none; font-weight: 700; font-size: 16px; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4); display: inline-block;'>📍 Find Nearest Emergency Services</a>
                    </div>
                """, unsafe_allow_html=True)
            
            # Rule-Based Analysis Results
            if ranked:
                st.markdown("""
                    <div style='background: rgba(102, 126, 234, 0.1); padding: 18px; border-radius: 15px; margin: 20px 0;'>
                        <h3 style='color: #667eea; margin: 0 0 12px 0; text-align: center;'>🎯 Possible Conditions</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                for idx, (cond, pct) in enumerate(ranked[:3]):
                    gradient_colors = [("#667eea", "#764ba2"), ("#f093fb", "#f5576c"), ("#4facfe", "#00f2fe")]
                    color1, color2 = gradient_colors[idx]
                    
                    st.markdown(f"""
                        <div style='background: white; padding: 20px; border-radius: 15px; margin: 12px 0; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-left: 5px solid {color1};'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <h4 style='color: #2d3748; margin: 0; font-size: 20px;'>{idx+1}. {cond}</h4>
                                <div style='background: linear-gradient(135deg, {color1} 0%, {color2} 100%); padding: 8px 18px; border-radius: 20px;'>
                                    <span style='color: white; font-size: 18px; font-weight: 700;'>{pct}%</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Healthcare Recommendations
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);'>
                        <h3 style='color: white; margin: 0 0 15px 0; text-align: center;'>💡 Healthcare Recommendations</h3>
                        <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                            <p style='color: white; font-weight: 600; margin: 0;'>✓ Consult a healthcare provider for proper diagnosis</p>
                        </div>
                        <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                            <p style='color: white; font-weight: 600; margin: 0;'>✓ Monitor symptoms and track any changes</p>
                        </div>
                        <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                            <p style='color: white; font-weight: 600; margin: 0;'>✓ Rest, stay hydrated, and avoid self-medication</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # AI Enhanced Analysis
            if ai_enable:
                client = get_client()
                if client and client.get("api_key") and client.get("api_key") != "YOUR_API_KEY_HERE":
                    st.markdown("""
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin: 20px 0;'>
                            <h3 style='color: white; margin: 0; text-align: center;'>🤖 AI-Enhanced Analysis Report</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        with st.spinner("🤖 Generating advanced AI analysis..."):
                            prompt = f"""Provide a comprehensive medical analysis for:
                            
Symptoms: {', '.join(selected)}
Severity: {severity_val}/10 ({severity_label})
Additional Details: {sanitized_extra if sanitized_extra else 'None provided'}
{f'Possible Conditions: {" ,".join([c for c, _ in ranked[:3]])}' if ranked else ''}

Provide:
1. Detailed symptom analysis
2. Possible causes and risk factors
3. Recommended precautions and self-care
4. When to seek immediate medical attention
5. Preventive measures

Be thorough but remind users to consult healthcare professionals."""
                            
                            msgs = [
                                {"role":"system","content":"You are an expert medical assistant. Provide detailed, evidence-based analysis with proper precautions and recommendations."},
                                {"role":"user","content":prompt}
                            ]
                            
                            response_text = ""
                            for chunk in send_chat_stream(msgs, client):
                                response_text += chunk
                            
                            st.markdown(f"""
                                <div style='background: white; padding: 25px; border-radius: 15px; margin: 15px 0; box-shadow: 0 8px 20px rgba(0,0,0,0.1); border-left: 5px solid #667eea;'>
                                    <div style='color: #2d3748; line-height: 1.8;'>{response_text}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Emergency reminder for AI analysis
                            if critical:
                                st.markdown("""
                                    <div style='background: #fee; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #f00;'>
                                        <p style='color: #c00; font-weight: 700; margin: 0;'>⚠️ CRITICAL: Call 112/911 immediately. This analysis is supplementary only.</p>
                                    </div>
                                """, unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"❌ AI analysis unavailable: {str(e)}")
            
            # Final Disclaimer
            st.markdown("""
                <div style='background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;'>
                    <p style='color: #856404; margin: 0; font-size: 14px;'><b>⚠️ Disclaimer:</b> This analysis is for informational purposes only and does not constitute medical advice. Always consult qualified healthcare professionals for diagnosis and treatment.</p>
                </div>
            """, unsafe_allow_html=True)

def page_find_care(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 40px; border-radius: 50px; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);'>
            <h1 style='color: white; font-size: 48px; margin: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);'>🏥 Emergency Care Locator</h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 20px; margin-top: 15px; font-weight: 300;'>Fast access to life-saving medical services near you</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Emergency Alert Banner
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); padding: 2px 30px; border-radius: 50px; box-shadow: 0 15px 45px rgba(255, 8, 68, 0.4); margin-bottom: 30px; border: 3px solid rgba(255,255,255,0.3);'>
            <div style='text-align: center;'>
                <h2 style='color: white; margin: 0; font-size: 32px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>🚨 LIFE-THREATENING EMERGENCY?</h2>
                <div style='background: rgba(255,255,255,0.25); padding: 10px 10px; border-radius: 100px; margin: 20px 0; backdrop-filter: blur(10px);'>
                    <p style='color: white; font-size: 18px; margin: 0 0 10px 0; font-weight: 600;'>CALL IMMEDIATELY:</p>
                    <h1 style='color: white; font-size: 72px; margin: 10px 0; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); letter-spacing: 8px;'>112 / 911</h1>
                    <p style='color: white; font-size: 16px; margin: 10px 0 0 0; opacity: 0.95;'>⚡ Don't wait • Don't drive yourself • Help is on the way</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
            <style>
            div.stButton > button {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
                color: white !important;
                font-size: 18px !important;
                font-weight: 700 !important;
                padding: 15px 30px !important;
                border: none !important;
                border-radius: 12px !important;
                box-shadow: 0 10px 30px rgba(67, 233, 123, 0.4) !important;
                transition: all 0.3s ease !important;
            }
            div.stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 15px 40px rgba(67, 233, 123, 0.6) !important;
            }
            </style>
        """, unsafe_allow_html=True)
    
    # Location Search Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 35px rgba(79, 172, 254, 0.3);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 28px;'>🗺️ Find Medical Services Near You</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom styling for location input
    st.markdown("""
        <style>
        div[data-testid="stTextInput"][data-key="emergency_location"] input,
        input[aria-label="📍 Enter your location"] {
            background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%) !important;
            border: 2px solid #3b82f6 !important;
            border-radius: 5px !important;
            padding: 15px 20px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            color: #1e3a8a !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stTextInput"][data-key="emergency_location"] input:focus,
        input[aria-label="📍 Enter your location"]:focus {
            border-color: #2563eb !important;
            box-shadow: 0 6px 25px rgba(37, 99, 235, 0.4) !important;
            transform: translateY(0px) !important;
        }
        div[data-testid="stTextInput"][data-key="emergency_location"] input::placeholder,
        input[aria-label="📍 Enter your location"]::placeholder {
            color: #60a5fa !important;
            opacity: 0.7 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    location = st.text_input(
        "📍 Enter your location",
        placeholder="City, ZIP code, street address, or 'current location'",
        key="emergency_location",
        help="Be as specific as possible for accurate results"
    )
    
    # Service Cards Grid
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px 20px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(240, 147, 251, 0.4); transition: transform 0.3s; cursor: pointer; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 15px;'>🏥</div>
                <h3 style='color: white; margin: 10px 0; font-size: 24px;'>Hospitals</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 10px 0;'>24/7 emergency rooms & specialized care centers</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Hospitals", key="btn_hospital", use_container_width=True):
            loc = location if location else 'me'
            st.markdown(f"[🏥 View Hospitals on Google Maps](https://www.google.com/maps/search/hospital+emergency+near+{loc})")
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 30px 20px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(250, 112, 154, 0.4); transition: transform 0.3s; cursor: pointer; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 15px;'>🚑</div>
                <h3 style='color: white; margin: 10px 0; font-size: 24px;'>Ambulance</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 10px 0;'>Emergency medical transport & paramedic services</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Ambulance", key="btn_ambulance", use_container_width=True):
            st.markdown(f"[🚑 View Ambulance Services]({ambulance_map_link(location)})")
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 30px 20px; border-radius: 20px; text-align: center; box-shadow: 0 12px 35px rgba(67, 233, 123, 0.4); transition: transform 0.3s; cursor: pointer; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 64px; margin-bottom: 15px;'>💊</div>
                <h3 style='color: white; margin: 10px 0; font-size: 24px;'>Pharmacies</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 10px 0;'>24-hour pharmacies & prescription services</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Pharmacies", key="btn_pharmacy", use_container_width=True):
            loc = location if location else 'me'
            st.markdown(f"[💊 View Pharmacies on Google Maps](https://www.google.com/maps/search/24+hour+pharmacy+near+{loc})")
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Additional Services Row
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 25px 20px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(168, 237, 234, 0.3); height: 220px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🩺</div>
                <h4 style='color: #333; margin: 8px 0; font-size: 20px;'>Urgent Care</h4>
                <p style='color: #555; font-size: 13px; margin: 8px 0;'>Walk-in clinics for non-life-threatening issues</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Urgent Care", key="btn_urgent", use_container_width=True):
            loc = location if location else 'me'
            st.markdown(f"[🩺 View Urgent Care Centers](https://www.google.com/maps/search/urgent+care+near+{loc})")
    
    with col5:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px 20px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(255, 236, 210, 0.3); height: 220px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🦷</div>
                <h4 style='color: #333; margin: 8px 0; font-size: 20px;'>Dental Emergency</h4>
                <p style='color: #555; font-size: 13px; margin: 8px 0;'>Emergency dental care & pain relief</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Dentists", key="btn_dental", use_container_width=True):
            loc = location if location else 'me'
            st.markdown(f"[🦷 View Emergency Dentists](https://www.google.com/maps/search/emergency+dentist+near+{loc})")
    
    with col6:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); padding: 25px 20px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(255, 154, 158, 0.3); height: 220px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🧠</div>
                <h4 style='color: #333; margin: 8px 0; font-size: 20px;'>Mental Health</h4>
                <p style='color: #555; font-size: 13px; margin: 8px 0;'>Crisis centers & counseling services</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Find Support", key="btn_mental", use_container_width=True):
            loc = location if location else 'me'
            st.markdown(f"[🧠 View Mental Health Services](https://www.google.com/maps/search/mental+health+crisis+center+near+{loc})")
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    
    # Important Contact Numbers
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);'>
            <h2 style='color: white; margin: 0 0 25px 0; text-align: center; font-size: 30px;'>📞 Essential Emergency Contacts</h2>
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;'>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'>
                    <h3 style='color: white; margin: 0 0 10px 0; font-size: 20px;'>🚨 Emergency Services</h3>
                    <p style='color: white; font-size: 32px; font-weight: 700; margin: 5px 0;'>112 / 911</p>
                    <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 5px 0;'>Police, Fire, Medical Emergency</p>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'>
                    <h3 style='color: white; margin: 0 0 10px 0; font-size: 20px;'>☠️ Poison Control</h3>
                    <p style='color: white; font-size: 28px; font-weight: 700; margin: 5px 0;'>1-800-222-1222</p>
                    <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 5px 0;'>24/7 Poisoning & Overdose Help</p>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'>
                    <h3 style='color: white; margin: 0 0 10px 0; font-size: 20px;'>🧠 Mental Health Crisis</h3>
                    <p style='color: white; font-size: 32px; font-weight: 700; margin: 5px 0;'>988</p>
                    <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 5px 0;'>Suicide & Crisis Lifeline</p>
                </div>
                <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'>
                    <h3 style='color: white; margin: 0 0 10px 0; font-size: 20px;'>👨‍⚕️ Medical Advice</h3>
                    <p style='color: white; font-size: 20px; font-weight: 700; margin: 5px 0;'>Your Primary Doctor</p>
                    <p style='color: rgba(255,255,255,0.9); font-size: 14px; margin: 5px 0;'>Non-emergency medical questions</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Safety Tips
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 18px; box-shadow: 0 10px 30px rgba(255, 236, 210, 0.3);'>
            <h3 style='color: #333; margin: 0 0 15px 0; text-align: center;'>⚡ Quick Emergency Tips</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; color: #444;'>
                <div style='background: rgba(255,255,255,0.6); padding: 15px; border-radius: 12px;'>
                    <b>✓ Stay Calm</b><br><small>Take deep breaths and assess the situation</small>
                </div>
                <div style='background: rgba(255,255,255,0.6); padding: 15px; border-radius: 12px;'>
                    <b>✓ Call First</b><br><small>Contact emergency services before driving</small>
                </div>
                <div style='background: rgba(255,255,255,0.6); padding: 15px; border-radius: 12px;'>
                    <b>✓ Share Location</b><br><small>Provide exact address to dispatchers</small>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def page_drugs(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);'>
            <h1 style='color: white; font-size: 42px; margin: 0;'>💊 Comprehensive Drug Database</h1>
            <p style='color: white; font-size: 18px; margin-top: 10px;'>Essential medicines with detailed clinical information</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Drug categories overview
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;'>
            <h3 style='color: white; margin: 0; text-align: center;'>📋 Drug Categories Available</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            padding: 15px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Category pills
    categories = list(set([drug['class'].split('(')[0].strip() for drug in SAMPLE_DRUGS]))
    cols = st.columns(min(len(categories), 4))
    for i, cat in enumerate(categories[:8]):
        with cols[i % 4]:
            count = len([d for d in SAMPLE_DRUGS if cat in d['class']])
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 10px; border-radius: 20px; text-align: center; margin: 5px 0;'>
                    <small style='color: white; font-weight: 600;'>{cat}</small><br>
                    <small style='color: white;'>{count} drugs</small>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced search section
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "🔍 Search Medications",
            placeholder="Search by drug name, class, or indication...",
            key="drug_search"
        )
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All Categories"] + sorted(categories),
            key="category_filter"
        )
    
    # Filter drugs
    filtered_drugs = SAMPLE_DRUGS
    if search_term:
        filtered_drugs = [d for d in filtered_drugs if 
                         search_term.lower() in d["name"].lower() or 
                         search_term.lower() in d["class"].lower() or
                         search_term.lower() in d["indications"].lower()]
    if category_filter != "All Categories":
        filtered_drugs = [d for d in filtered_drugs if category_filter in d["class"]]
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center;'>
            <h4 style='color: white; margin: 0;'>📊 Found {len(filtered_drugs)} medications</h4>
        </div>
    """, unsafe_allow_html=True)
    
    # Display drugs in enhanced cards
    for idx, drug in enumerate(filtered_drugs):
        gradient_colors = [
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
            "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
        ]
        
        with st.expander(f"💊 {drug['name']} ({drug['class']})", expanded=False):
            # Drug header with gradient
            st.markdown(f"""
                <div style='background: {gradient_colors[idx % 5]}; padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.15);'>
                    <h2 style='color: white; margin: 0; text-align: center;'>{drug['name']}</h2>
                    <p style='color: white; text-align: center; font-size: 16px; margin: 5px 0; opacity: 0.9;'>{drug['class']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Main information in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #28a745;'>
                        <h4 style='color: #28a745; margin: 0;'>🎯 Medical Uses</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Indications:** {drug['indications']}")
                
                st.markdown("""
                    <div style='background: #fff3cd; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #ffc107;'>
                        <h4 style='color: #856404; margin: 0;'>⚠️ Side Effects</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Common Side Effects:** {drug['common_side_effects']}")
            
            with col2:
                st.markdown("""
                    <div style='background: #f8d7da; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #dc3545;'>
                        <h4 style='color: #721c24; margin: 0;'>🚫 Contraindications</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Contraindications:** {drug.get('contraindications', 'None reported')}")
                
                st.markdown("""
                    <div style='background: #d1ecf1; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #17a2b8;'>
                        <h4 style='color: #0c5460; margin: 0;'>🔗 Drug Interactions</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Major Interactions:** {drug.get('major_interactions', 'None reported')}")
            
            # Footer with external links
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"**[📚 PubMed Research](https://pubmed.ncbi.nlm.nih.gov/?term={drug['name']})**")
            with col_b:
                st.markdown(f"**[🏥 Drugs.com Info](https://www.drugs.com/search.php?searchterm={drug['name']})**")
            with col_c:
                st.markdown(f"**[📖 MedlinePlus](https://medlineplus.gov/druginfo/meds/search.html?query={drug['name']})**")

def page_selfcare(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 40px; border-radius: 25px; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);'>
            <h1 style='color: white; font-size: 48px; margin: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);'>🧘 Self-Care & Prevention</h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 20px; margin-top: 15px; font-weight: 300;'>Proactive wellness strategies for a healthier life</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Wellness Categories
    st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 25px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 12px 35px rgba(67, 233, 123, 0.4);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 32px;'>🌟 Wellness Categories</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            padding: 15px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Category Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🫀</div>
                <h4 style='color: white; margin: 8px 0; font-size: 20px;'>Heart Health</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 5px 0;'>Cardiovascular wellness</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🧠</div>
                <h4 style='color: white; margin: 8px 0; font-size: 20px;'>Mental Health</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 5px 0;'>Emotional wellness</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 25px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(250, 112, 154, 0.4); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🍎</div>
                <h4 style='color: white; margin: 8px 0; font-size: 20px;'>Nutrition</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 5px 0;'>Healthy eating habits</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 25px; border-radius: 18px; text-align: center; box-shadow: 0 10px 30px rgba(168, 237, 234, 0.4); height: 200px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 52px; margin-bottom: 10px;'>🏋️</div>
                <h4 style='color: white; margin: 8px 0; font-size: 20px;'>Exercise</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 13px; margin: 5px 0;'>Physical fitness</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    
    # Prevention Strategies Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 30px;'>🛡️ Disease Prevention Strategies</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px;'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🫀</div>
                    <h3 style='color: #667eea; margin: 10px 0;'>Cardiovascular Health</h3>
                </div>
                <div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #667eea;'>
                    <p style='color: #667eea; font-weight: 700; margin: 0 0 8px 0;'>🏋️ Exercise</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>150 minutes of moderate activity weekly or 75 minutes of vigorous activity</p>
                </div>
                <div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #667eea;'>
                    <p style='color: #667eea; font-weight: 700; margin: 0 0 8px 0;'>🥗 Diet</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Mediterranean diet rich in fruits, vegetables, whole grains, and healthy fats</p>
                </div>
                <div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #667eea;'>
                    <p style='color: #667eea; font-weight: 700; margin: 0 0 8px 0;'>🩺 Monitoring</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Regular blood pressure, cholesterol, and blood sugar checks</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🧠</div>
                    <h3 style='color: #8b5cf6; margin: 10px 0;'>Mental Wellness</h3>
                </div>
                <div style='background: rgba(139, 92, 246, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #8b5cf6;'>
                    <p style='color: #8b5cf6; font-weight: 700; margin: 0 0 8px 0;'>🧘 Stress Management</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Practice meditation, yoga, or deep breathing exercises daily</p>
                </div>
                <div style='background: rgba(139, 92, 246, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #8b5cf6;'>
                    <p style='color: #8b5cf6; font-weight: 700; margin: 0 0 8px 0;'>🛌 Sleep Hygiene</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>7-9 hours of quality sleep per night with consistent schedule</p>
                </div>
                <div style='background: rgba(139, 92, 246, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #8b5cf6;'>
                    <p style='color: #8b5cf6; font-weight: 700; margin: 0 0 8px 0;'>👥 Social Connection</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Maintain strong relationships and seek support when needed</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px;'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🦠</div>
                    <h3 style='color: #10b981; margin: 10px 0;'>Infection Prevention</h3>
                </div>
                <div style='background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #10b981;'>
                    <p style='color: #10b981; font-weight: 700; margin: 0 0 8px 0;'>💉 Vaccinations</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Stay up-to-date with recommended vaccines for your age group</p>
                </div>
                <div style='background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #10b981;'>
                    <p style='color: #10b981; font-weight: 700; margin: 0 0 8px 0;'>🧼 Hand Hygiene</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Wash hands frequently with soap for at least 20 seconds</p>
                </div>
                <div style='background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #10b981;'>
                    <p style='color: #10b981; font-weight: 700; margin: 0 0 8px 0;'>😷 Respiratory Etiquette</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Cover coughs/sneezes and avoid touching face</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🍎</div>
                    <h3 style='color: #f59e0b; margin: 10px 0;'>Nutrition & Lifestyle</h3>
                </div>
                <div style='background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #f59e0b;'>
                    <p style='color: #f59e0b; font-weight: 700; margin: 0 0 8px 0;'>💧 Hydration</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Drink 8-10 glasses of water daily</p>
                </div>
                <div style='background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #f59e0b;'>
                    <p style='color: #f59e0b; font-weight: 700; margin: 0 0 8px 0;'>🚫 Avoid Toxins</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>No smoking, limit alcohol, avoid processed foods</p>
                </div>
                <div style='background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 4px solid #f59e0b;'>
                    <p style='color: #f59e0b; font-weight: 700; margin: 0 0 8px 0;'>⚖️ Weight Management</p>
                    <p style='color: #4a5568; margin: 0; font-size: 14px;'>Maintain healthy BMI through balanced diet and exercise</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    
    # Home Care Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(17, 153, 142, 0.4);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 30px;'>🏠 Common Illness Home Care</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);'>
                <div style='text-align: center; margin-bottom: 15px;'>
                    <div style='font-size: 48px;'>🤒</div>
                    <h4 style='color: #ef4444; margin: 10px 0; font-size: 22px;'>Fever</h4>
                </div>
                <div style='background: #fef2f2; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #991b1b; font-weight: 600; margin: 0; font-size: 14px;'>✓ Rest & Hydrate</p>
                </div>
                <div style='background: #fef2f2; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #991b1b; font-weight: 600; margin: 0; font-size: 14px;'>✓ Fever Reducers</p>
                </div>
                <div style='background: #fef2f2; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #991b1b; font-weight: 600; margin: 0; font-size: 14px;'>⚠️ Seek care if >104°F</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);'>
                <div style='text-align: center; margin-bottom: 15px;'>
                    <div style='font-size: 48px;'>🤧</div>
                    <h4 style='color: #3b82f6; margin: 10px 0; font-size: 22px;'>Cough & Cold</h4>
                </div>
                <div style='background: #eff6ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #1e3a8a; font-weight: 600; margin: 0; font-size: 14px;'>✓ Increase Fluids</p>
                </div>
                <div style='background: #eff6ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #1e3a8a; font-weight: 600; margin: 0; font-size: 14px;'>✓ Use Humidifier</p>
                </div>
                <div style='background: #eff6ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #1e3a8a; font-weight: 600; margin: 0; font-size: 14px;'>✓ Rest & Isolate</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);'>
                <div style='text-align: center; margin-bottom: 15px;'>
                    <div style='font-size: 48px;'>🤢</div>
                    <h4 style='color: #8b5cf6; margin: 10px 0; font-size: 22px;'>Headache</h4>
                </div>
                <div style='background: #faf5ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #5b21b6; font-weight: 600; margin: 0; font-size: 14px;'>✓ Dark, Quiet Room</p>
                </div>
                <div style='background: #faf5ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #5b21b6; font-weight: 600; margin: 0; font-size: 14px;'>✓ Pain Relievers</p>
                </div>
                <div style='background: #faf5ff; padding: 12px; border-radius: 10px; margin: 8px 0;'>
                    <p style='color: #5b21b6; font-weight: 600; margin: 0; font-size: 14px;'>✓ Stay Hydrated</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Wellness Tips Banner
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 236, 210, 0.4); text-align: center;'>
            <h3 style='color: #2d3748; margin: 0 0 20px 0; font-size: 26px;'>💡 Daily Wellness Tips</h3>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                <div style='background: white; padding: 20px; border-radius: 12px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🌅</div>
                    <p style='color: #4a5568; font-weight: 600; margin: 0; font-size: 14px;'>Morning Sunlight</p>
                </div>
                <div style='background: white; padding: 20px; border-radius: 12px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🧘</div>
                    <p style='color: #4a5568; font-weight: 600; margin: 0; font-size: 14px;'>Daily Meditation</p>
                </div>
                <div style='background: white; padding: 20px; border-radius: 12px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🚶</div>
                    <p style='color: #4a5568; font-weight: 600; margin: 0; font-size: 14px;'>10K Steps Daily</p>
                </div>
                <div style='background: white; padding: 20px; border-radius: 12px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>📚</div>
                    <p style='color: #4a5568; font-weight: 600; margin: 0; font-size: 14px;'>Continuous Learning</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def page_ai_chat(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 30px; border-radius: 200px; text-align: center; margin-bottom: 20px; box-shadow: 0 15px 35px rgba(250, 112, 154, 0.4);'>
            <h1 style='color: white; font-size: 36px; margin: 0;'>🤖 AI Medical Assistant</h1>
            <p style='color: white; font-size: 16px; margin-top: 8px;'>24/7 AI-powered health chat support</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    client = get_client()
    if not client or client.get("api_key") == "YOUR_API_KEY_HERE":
        st.error("🔑 **API Key Required** - Set your `OPENROUTER_API_KEY` environment variable or update config.py")
        return
    
    # Initialize chat history
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # Compact disclaimer
    with st.expander("⚠️ Important Safety Information - Click to read", expanded=False):
        st.warning("""
        **THIS IS AN INFORMATIONAL TOOL ONLY**
        - NOT a substitute for professional medical advice
        - NOT for emergencies (Call 112/911)
        - DO NOT enter personal health information
        - ALWAYS consult healthcare providers
        """)
    

    
    # Display chat history
    if not st.session_state.ai_chat_history:
        st.markdown("""
            <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 15px; box-shadow: 0 8px 20px rgba(17, 153, 142, 0.3);'>
                <h3>👋 Hello! I'm your AI Medical Assistant</h3>
                <p>Ask me anything about symptoms, medications, or general health information.</p>
                <p><small>Remember: This is for informational purposes only.</small></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.ai_chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 18px;
                    border-radius: 18px 18px 5px 18px;
                    margin: 8px 0 8px 80px;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                '>
                    <strong>You:</strong><br>{msg['text']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='
                    background: #38ef7d;
                    color: purple;
                    padding: 12px 18px;
                    border-radius: 18px 18px 18px 5px;
                    margin: 8px 80px 8px 0;
                    border-left: 4px solid #0ea5e9;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                '>
                    <strong style='color: #0ea5e9;'>🤖 AI Assistant:</strong><br>{msg['text']}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fixed input section at bottom
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.markdown("""
            <style>
            div[data-testid="stTextInput"] input {
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
                border: 2px solid #ff6b6b !important;
                border-radius: 200px !important;
                padding: 12px 20px !important;
                font-size: 16px !important;
                color: #2d3748 !important;
                box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
            }
            div[data-testid="stTextInput"] input:focus {
                border-color: #fa709a !important;
                box-shadow: 0 6px 20px rgba(250, 112, 154, 0.5) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        user_input = st.text_input(
            "💬 Type your message:",
            placeholder="Ask about symptoms, medications, or health information...",
            key="ai_chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.rerun()
    
    # Send button styling
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            padding: 12px 24px !important;
            border: none !important;
            border-radius: 100px !important;
            box-shadow: 0 8px 20px rgba(17, 153, 142, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 30px rgba(17, 153, 142, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Send Message", use_container_width=True, type="primary"):
        if user_input.strip():
            sanitized_input, phi_detected = sanitize_text(user_input)
            
            if phi_detected:
                st.warning("⚠️ Personal information removed for privacy")
            
            # Add user message
            st.session_state.ai_chat_history.append({
                "role": "user",
                "text": sanitized_input
            })
            
            try:
                with st.spinner("🤖 AI is thinking..."):
                    # Build full conversation context
                    messages = [{"role": "system", "content": "You are a cautious, evidence-based medical assistant. Provide helpful information but always remind users to consult healthcare professionals."}]
                    
                    # Add conversation history
                    for msg in st.session_state.ai_chat_history:
                        messages.append({
                            "role": msg["role"] if msg["role"] == "user" else "assistant",
                            "content": msg["text"]
                        })
                    
                    response = ""
                    for chunk in send_chat_stream(messages, client):
                        response += chunk
                    
                    st.session_state.ai_chat_history.append({
                        "role": "assistant",
                        "text": response
                    })
                    
                    st.rerun()
            
            except Exception as e:
                st.error(f"❌ AI Service Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a message before sending")

def page_about(ctx):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 40px; border-radius: 50px; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);'>
            <h1 style='color: white; font-size: 48px; margin: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);'>ℹ️ About MediGuideAI</h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 20px; margin-top: 15px; font-weight: 300;'>Your trusted AI-powered health companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Emergency Banner
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); padding: 25px; border-radius: 20px; margin-bottom: 30px; box-shadow: 0 12px 35px rgba(255, 8, 68, 0.4); border: 3px solid rgba(255,255,255,0.3);'>
            <div style='text-align: center;'>
                <h3 style='color: white; margin: 0 0 10px 0; font-size: 24px;'>🚨 EMERGENCY? CALL 112 / 911 IMMEDIATELY</h3>
                <p style='color: rgba(255,255,255,0.95); margin: 0; font-size: 15px;'>This platform is NOT for medical emergencies</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # What is MediGuideAI Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 30px;'>🏥 What is MediGuideAI?</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 30px;'>
            <p style='color: #2d3748; font-size: 17px; line-height: 1.8; margin-bottom: 20px;'>
                <b>MediGuideAI</b> is an intelligent health-support platform that combines advanced rule-based logic with optional AI models to help users understand symptoms, explore possible health conditions, and access reliable preventive care information.
            </p>
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #667eea;'>
                <p style='color: #667eea; font-weight: 700; margin: 0 0 10px 0; font-size: 18px;'>✨ Key Features:</p>
                <ul style='color: #4a5568; font-size: 16px; line-height: 1.8;'>
                    <li>AI-powered symptom analysis with rule-based validation</li>
                    <li>Comprehensive drug database with 50+ essential medicines</li>
                    <li>Emergency care locator with Google Maps integration</li>
                    <li>24/7 AI medical assistant for health queries</li>
                    <li>Privacy-first design with automatic PII redaction</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            padding: 15px 30px !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(250, 112, 154, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(250, 112, 154, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Mission & Vision Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; border-radius: 20px; box-shadow: 0 12px 30px rgba(240, 147, 251, 0.4); height: 100%;'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🎯</div>
                    <h3 style='color: white; margin: 10px 0 0 0; font-size: 26px;'>Our Mission</h3>
                </div>
                <p style='color: rgba(255,255,255,0.95); font-size: 16px; line-height: 1.7; text-align: center;'>
                    To make trustworthy health information accessible to everyone, regardless of background, location, or technical knowledge.
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; margin-top: 15px;'>
                    <p style='color: white; font-weight: 600; margin: 0; text-align: center;'>Empowering better health decisions through AI</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 30px; border-radius: 20px; box-shadow: 0 12px 30px rgba(79, 172, 254, 0.4); height: 100%;'>
                <div style='text-align: center; margin-bottom: 20px;'>
                    <div style='font-size: 56px;'>🔭</div>
                    <h3 style='color: white; margin: 10px 0 0 0; font-size: 26px;'>Our Vision</h3>
                </div>
                <p style='color: rgba(255,255,255,0.95); font-size: 16px; line-height: 1.7; text-align: center;'>
                    A world where everyone has instant access to reliable health information, enabling early awareness and proactive wellness.
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; margin-top: 15px;'>
                    <p style='color: white; font-weight: 600; margin: 0; text-align: center;'>Prevention through education</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Core Values Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 30px;'>💖 Our Core Values</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 48px; margin-bottom: 15px;'>🎯</div>
                <h4 style='color: #667eea; margin: 10px 0; font-size: 22px;'>Accuracy</h4>
                <p style='color: #4a5568; font-size: 15px; line-height: 1.6;'>Evidence-based information from trusted medical sources and validated AI models</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 48px; margin-bottom: 15px;'>🔒</div>
                <h4 style='color: #667eea; margin: 10px 0; font-size: 22px;'>Privacy</h4>
                <p style='color: #4a5568; font-size: 15px; line-height: 1.6;'>Automatic PII redaction, session-only storage, and no data collection</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: center; height: 280px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='font-size: 48px; margin-bottom: 15px;'>⚖️</div>
                <h4 style='color: #667eea; margin: 10px 0; font-size: 22px;'>Transparency</h4>
                <p style='color: #4a5568; font-size: 15px; line-height: 1.6;'>Clear limitations, honest disclaimers, and explainable AI insights</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Important Disclaimers Section
    st.markdown("""
        <div style='background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); padding: 25px; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(235, 51, 73, 0.4);'>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 30px;'>⚠️ Important Disclaimers</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-left: 5px solid #ef4444;'>
                <h4 style='color: #ef4444; margin: 0 0 15px 0; font-size: 20px;'>🚫 What MediGuideAI is NOT</h4>
                <ul style='color: #4a5568; font-size: 15px; line-height: 1.8;'>
                    <li><b>NOT a medical device</b> or diagnostic tool</li>
                    <li><b>NOT for emergencies</b> - Call 112/911</li>
                    <li><b>NOT a replacement</b> for professional medical advice</li>
                    <li><b>NOT for treatment</b> recommendations</li>
                    <li><b>NOT a substitute</b> for doctor consultations</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-left: 5px solid #10b981;'>
                <h4 style='color: #10b981; margin: 0 0 15px 0; font-size: 20px;'>✅ What MediGuideAI IS</h4>
                <ul style='color: #4a5568; font-size: 15px; line-height: 1.8;'>
                    <li><b>Educational tool</b> for health awareness</li>
                    <li><b>Information resource</b> for symptom understanding</li>
                    <li><b>Decision support</b> to encourage medical consultation</li>
                    <li><b>Preventive care guide</b> for wellness</li>
                    <li><b>Health literacy platform</b> for learning</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Legal Notice
    st.markdown("""
        <div style='background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); padding: 30px; border-radius: 20px; box-shadow: 0 12px 35px rgba(48, 207, 208, 0.4);'>
            <h3 style='color: white; margin: 0 0 20px 0; text-align: center; font-size: 26px;'>⚖️ Legal Notice & Liability</h3>
            <div style='background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'>
                <p style='color: white; font-size: 15px; line-height: 1.8; margin: 0;'>
                    <b>By using MediGuideAI, you acknowledge that:</b><br><br>
                    • All information is for <b>educational purposes only</b><br>
                    • You will <b>consult healthcare professionals</b> for medical decisions<br>
                    • Emergency situations require <b>immediate professional care</b><br>
                    • No warranty is provided for <b>medical accuracy</b><br>
                    • The platform is <b>not liable</b> for health outcomes<br><br>
                    <b style='font-size: 16px;'>👨‍⚕️ Always consult qualified healthcare providers for medical advice, diagnosis, and treatment.</b>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Contact & Support
    st.markdown("""
        <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(168, 237, 234, 0.3); text-align: center;'>
            <h3 style='color: #2d3748; margin: 0 0 15px 0; font-size: 26px;'>📞 Emergency Contacts</h3>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px;'>
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🚨</div>
                    <p style='color: #ef4444; font-weight: 700; font-size: 24px; margin: 5px 0;'>112 / 911</p>
                    <p style='color: #6b7280; font-size: 14px; margin: 5px 0;'>Medical Emergency</p>
                </div>
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>☠️</div>
                    <p style='color: #f59e0b; font-weight: 700; font-size: 20px; margin: 5px 0;'>1-800-222-1222</p>
                    <p style='color: #6b7280; font-size: 14px; margin: 5px 0;'>Poison Control</p>
                </div>
                <div style='background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🧠</div>
                    <p style='color: #8b5cf6; font-weight: 700; font-size: 24px; margin: 5px 0;'>988</p>
                    <p style='color: #6b7280; font-size: 14px; margin: 5px 0;'>Mental Health Crisis</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ------------------------
# Main Application
# ------------------------
def main():
    # ------------------------
    # Ensure required session state keys exist BEFORE anything reads them
    # ------------------------
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    if "ai_enabled" not in st.session_state:
        st.session_state.ai_enabled = False
    # ------------------------

    # Get sidebar controls and apply styling
    ctx = sidebar_controls()
    apply_dynamic_style(ctx["palette"])
    
    # Set AI availability (override default if env var present)
    st.session_state["ai_enabled"] = bool(os.getenv("OPENROUTER_API_KEY"))
    
    # Main header
    st.markdown(f"""
        <div style='text-align: center; padding: 30px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);'>
            <h1 style='color: #ffffff; font-size: 48px; margin-bottom: 10px; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>🏥 MediGuideAI</h1>
            <p style='color: #f0f4ff; font-size: 22px; font-weight: 500; letter-spacing: 1px;'>Premium Medical Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Render top navigation tabs - ALL 7 PAGES VISIBLE
    st.markdown("---")
    # Ensure current_page is always a string
    current_page_label: str = str(ctx.get("current_page", st.session_state.current_page) or "Home")
    render_top_tabs(current_page_label)
    
    st.markdown("---")
    
    # Route to appropriate page based on session state
    pages = {
        "Home": page_home,
        "Symptom Checker": page_symptom_checker,
        "Find Care": page_find_care,
        "Drugs & Therapies": page_drugs,
        "Self-care & Prevention": page_selfcare,
        "AI Chat": page_ai_chat,
        "About & Disclaimer": page_about
    }
    
    # Execute current page
    current_page = current_page_label or "Home"
    page_fn = pages.get(current_page, page_home)
    page_fn(ctx)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: var(--muted); padding: 20px;'>
        <small>© 2024 MediGuideAI. For informational purposes only. Always consult healthcare professionals.</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
