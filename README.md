# MediGuideAI

**Premium Medical Intelligence Platform**  
*AI-powered symptom analysis + comprehensive drug database + emergency care locator*

> **Important:** MediGuideAI is an educational demo and **not** a medical device. It does **not** provide clinical diagnoses or treatment. If you are experiencing a medical emergency, call your local emergency number immediately.

---

## 🏥 Overview

MediGuideAI is a sophisticated Streamlit-based medical information platform featuring:

- **🩺 Advanced Symptom Checker** - AI-powered analysis with rule-based validation using comprehensive `rules.json`
- **💊 Enhanced Drug Database** - 50+ essential medicines with detailed clinical information, category filtering, and external research links
- **📍 Emergency Care Locator** - Quick access to nearby medical services with Google Maps integration
- **🧘 Self-Care & Prevention** - Health maintenance strategies and preventive care guidance
- **🤖 AI Medical Assistant** - Claude 3.5 Sonnet integration for 24/7 health chat support
- **🔒 Privacy-First Design** - Automatic PII redaction, session-only storage, and explicit consent
- **🎨 Dynamic Theme System** - 6 customizable color palettes with responsive design
- **♿ Accessibility Features** - High-contrast themes, keyboard navigation, and mobile optimization

---

## 🚀 Features

### Core Pages
1. **Home** - Interactive dashboard with health metrics, feature overview, and quick access cards
2. **Symptom Checker** - AI-powered analysis with emergency symptom alerts and severity assessment
3. **Find Care** - Emergency services locator with Google Maps integration and important contact numbers
4. **Drugs & Therapies** - Enhanced searchable database with category pills, advanced filtering, and external research links
5. **Self-Care & Prevention** - Comprehensive disease prevention strategies and home care guidance
6. **AI Chat** - 24/7 medical assistant with conversation history and privacy protection
7. **About & Disclaimer** - Legal information, usage terms, and safety guidelines

### Advanced Features
- **Intelligent Symptom Analysis** - Combines rule-based scoring with AI insights for comprehensive assessment
- **Critical Condition Detection** - Automatic alerts for potentially serious conditions requiring immediate care
- **Enhanced Drug Information** - Color-coded sections for medical uses, side effects, contraindications, and interactions
- **Privacy Protection** - Real-time PII detection and redaction (emails, phone numbers, IDs)
- **Dynamic Theming** - 6 professional color palettes with dark sidebar and gradient designs
- **External Integration** - Direct links to PubMed, Drugs.com, and MedlinePlus for additional research
- **Responsive Design** - Optimized for desktop and mobile with touch-friendly interfaces

---

## 📁 Project Structure

```
MediGuideAI/
├── app.py                 # Main application launcher
├── ui.py                  # Streamlit UI with 7 pages and navigation
├── config.py              # OpenRouter API configuration
├── medical_data.py        # Sample diseases and comprehensive drug database
├── rules.json             # Symptom-to-condition mapping rules
├── rules/
│   ├── __init__.py        # Package initialization
│   └── rules_loader.py    # JSON rules validation and loading
└── README.md              # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Required packages: `requests`, `pandas`

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MediGuideAI
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests pandas
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

### AI Chat Setup (Optional)
For AI-powered features, set your OpenRouter API key:

**Option 1: Environment Variable**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

**Option 2: Update config.py**
```python
OPENROUTER_API_KEY = "your-api-key-here"
```

---

## 🔧 Configuration

### Theme Customization
The application supports 6 built-in themes accessible via the sidebar:
- **Teal** (default) - Professional medical theme
- **Blue** - Clean corporate look
- **Warm** - Friendly orange tones
- **Purple** - Modern gradient style
- **Green** - Natural health theme
- **Coral** - Vibrant accent colors

### Rules Customization
Edit `rules.json` to modify symptom-to-condition mappings with confidence weights:

```json
{
  "rules": {
    "fever": {
      "Common Cold": 2,
      "Flu": 4,
      "COVID-19": 1,
      "Pneumonia": 5,
      "Malaria": 5,
      "Sepsis": 5
    },
    "chest pain": {
      "Ischemic Heart Disease": 5,
      "Myocardial Infarction": 5,
      "Pulmonary Embolism": 5
    }
  }
}
```

### Comprehensive Drug Database
The `medical_data.py` file contains 50+ essential medicines organized by therapeutic categories:
- **Anesthetic Agents** - Halothane, Ketamine, Propofol, Lignocaine
- **Analgesics/NSAIDs** - Aspirin, Diclofenac, Paracetamol, Morphine
- **Antiallergics** - Adrenaline, Cetirizine, Dexamethasone
- **Anticonvulsants** - Carbamazepine, Diazepam, Sodium valproate
- **Anti-infectives** - Amoxicillin, Azithromycin, Ciprofloxacin, Fluconazole
- **Cardiovascular** - Amlodipine, Atenolol, Enalapril, Atorvastatin
- **Gastrointestinal** - Omeprazole, Ranitidine, Domperidone
- **Hormones/Endocrine** - Insulin, Metformin, Levothyroxine
- **Psychotherapeutic** - Haloperidol, Amitriptyline, Fluoxetine
- **Respiratory** - Salbutamol, Budesonide

---

## 🎯 Usage

### Symptom Analysis
1. Navigate to **Symptom Checker**
2. Enter symptoms manually or select from suggestions
3. Add additional details and severity level
4. Enable AI Analysis for enhanced insights
5. Review rule-based matches and AI recommendations

### Drug Information
1. Go to **Drugs & Therapies**
2. Browse category pills or use enhanced search (name, class, indication)
3. Apply category filters for targeted results
4. Click on any drug to view comprehensive information:
   - **Medical Uses** - Detailed indications and therapeutic applications
   - **Side Effects** - Common adverse reactions and warnings
   - **Contraindications** - When not to use the medication
   - **Drug Interactions** - Major interactions and precautions
   - **External Research** - Direct links to PubMed, Drugs.com, and MedlinePlus

### Emergency Services
1. Visit **Find Care** page
2. Enter your location
3. Access quick links to hospitals and ambulance services
4. View important emergency contact numbers

---

## 🔒 Privacy & Safety

### Privacy Protection
- **Real-time PII Redaction**: Automatic detection and removal of emails, phone numbers, and ID numbers
- **Session-Only Storage**: Chat history and user data stored only in browser session
- **No Persistent Data**: No user information saved to disk or external servers
- **Local Processing**: Rule-based symptom analysis performed entirely locally
- **Sanitized AI Requests**: All AI communications automatically sanitized before transmission

### Safety Disclaimers
- ⚠️ **Not a medical device** - For informational purposes only
- 🚨 **Emergency situations** - Always call 112/911 for emergencies
- 👨‍⚕️ **Professional consultation** - Always consult healthcare providers
- 📚 **Educational use** - Designed for learning and awareness only

---

## 🤖 AI Integration

### Supported Models
- **Primary**: Claude 3.5 Sonnet (via OpenRouter)
- **Fallback**: Rule-based analysis when AI unavailable

### AI Features
- **Enhanced Symptom Analysis** - Comprehensive assessment when rule-based matching is insufficient
- **24/7 Medical Chat** - Interactive health assistant with conversation history
- **Privacy-Aware Processing** - Automatic PII sanitization before AI communication
- **Contextual Health Information** - Personalized responses based on symptom severity and details
- **Fallback Support** - Graceful degradation to rule-based analysis when AI unavailable

---

## 🎨 UI/UX Features

### Modern Design
- **Dynamic Gradient System** - Eye-catching headers and section dividers with 5 rotating color schemes
- **Enhanced Card Layout** - Color-coded information sections with hover effects and shadows
- **Professional Sidebar** - Dark gradient theme with high contrast and improved readability
- **Responsive Grid System** - Optimized layouts for desktop, tablet, and mobile devices
- **Interactive Elements** - Smooth transitions, hover effects, and visual feedback

### Accessibility & UX
- **Keyboard Navigation** - Full keyboard support with visible focus indicators
- **High Contrast Themes** - Multiple color palettes for improved readability
- **Screen Reader Support** - Semantic HTML structure and proper ARIA labels
- **Mobile Optimization** - Touch-friendly interfaces with responsive breakpoints
- **Visual Hierarchy** - Clear information organization with consistent styling

---

## 📊 Data Sources

### Medical Information
- **Comprehensive Drug Database**: 50+ essential medicines based on WHO Essential Medicine Lists
- **Extensive Symptom Rules**: 100+ symptoms mapped to medical conditions with confidence weights
- **Clinical References**: Information sourced from medical literature and clinical guidelines
- **External Integration**: Direct links to PubMed research, Drugs.com, and MedlinePlus

### Data Validation & Security
- **Structured JSON Validation**: Robust rules loading with error handling via `rules_loader.py`
- **Input Sanitization**: Real-time PII detection and redaction using regex patterns
- **Error Handling**: Graceful fallbacks for missing data and API failures
- **Type Safety**: Python type hints throughout codebase for better reliability

---

## 🚀 Development

### Adding New Features
1. **New Pages**: Add page functions to `ui.py` and update navigation in `render_top_tabs()`
2. **Drug Entries**: Extend `SAMPLE_DRUGS` list in `medical_data.py` with complete drug information
3. **Symptom Rules**: Update `rules.json` with new symptom-to-condition mappings and confidence weights
4. **Themes**: Add new color palettes to `PALETTES` dictionary with gradient definitions
5. **AI Models**: Modify `config.py` to support additional OpenRouter models

### Advanced Code Structure
- **Modular Architecture**: Clean separation between UI (`ui.py`), configuration (`config.py`), data (`medical_data.py`), and rules (`rules/`)
- **Dynamic Styling**: CSS-in-Python approach with theme system and responsive design
- **Error Handling**: Comprehensive exception management with graceful fallbacks
- **Type Safety**: Full Python type hints for better code quality and IDE support
- **Privacy by Design**: Built-in PII sanitization and session-only data storage

---

## ⚖️ Legal & Compliance

### Disclaimer
This application is provided for **educational and informational purposes only**. It is not intended to:
- Replace professional medical advice
- Provide clinical diagnoses or treatment recommendations
- Be used in emergency medical situations
- Substitute for consultation with qualified healthcare providers

### Liability
Users acknowledge that:
- All medical decisions should involve healthcare professionals
- The application provides general information only
- Emergency situations require immediate professional care
- No warranty is provided for medical accuracy

---

## 📞 Support & Contact

### Emergency
- **Medical Emergency**: Call 112 / 911 immediately
- **Poison Control**: 1-800-222-1222
- **Mental Health Crisis**: 988

### Technical Support
- Review documentation in this README
- Check `rules.json` format for symptom mapping issues
- Verify API key configuration for AI features
- Ensure all dependencies are properly installed

---

## 🔄 Version History

### Current Version Features
- **Comprehensive Medical Database**: 50+ essential medicines with detailed clinical information
- **Advanced Symptom Analysis**: AI-powered assessment with rule-based validation and critical condition detection
- **Enhanced User Interface**: Modern gradient design with 6 dynamic themes and responsive layouts
- **Intelligent Search**: Multi-field drug search with category filtering and visual category pills
- **Privacy Protection**: Real-time PII redaction, session-only storage, and sanitized AI communication
- **Professional Design**: Dark sidebar, gradient headers, color-coded information sections
- **External Integration**: Direct links to PubMed, Drugs.com, and MedlinePlus for additional research
- **Accessibility**: High-contrast themes, keyboard navigation, and mobile optimization

---

**© 2024 MediGuideAI. For informational purposes only. Always consult healthcare professionals.**
