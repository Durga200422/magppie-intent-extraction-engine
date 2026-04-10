import sys
import os

# Add the current directory to sys.path so 'src' can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
from src.extractor import extract_kitchen_intent
from src.utils import load_history
import base64
import json

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Magppie AI Showroom",
    layout="wide",
    page_icon="🔧",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS FOR PREMIUM UI
# ============================================================================
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:wght@700&display=swap');
    
    /* Root Variables - Magppie Brand Colors */
    :root {
        --primary-black: #000000;
        --primary-white: #FFFFFF;
        --accent-gold: #D4AF37;
        --bg-dark: #0A0A0A;
        --bg-card: #1A1A1A;
        --text-gray: #B0B0B0;
        --border-gray: #2A2A2A;
        --success-green: #10B981;
        --warning-amber: #F59E0B;
        --error-red: #EF4444;
    }
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .magppie-header {
        background: linear-gradient(90deg, rgba(0,0,0,0.95) 0%, rgba(26,26,26,0.95) 100%);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid var(--border-gray);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    .magppie-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-gold) 0%, transparent 100%);
    }
    
    .magppie-logo {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--primary-white);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 20px rgba(212, 175, 55, 0.3);
    }
    
    .magppie-tagline {
        font-size: 1rem;
        color: var(--accent-gold);
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 0.3em;
        font-weight: 300;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid var(--border-gray);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: var(--text-gray);
        font-size: 1.1rem;
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--accent-gold);
        background-color: rgba(212, 175, 55, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--accent-gold);
        border-bottom: 3px solid var(--accent-gold);
    }
    
    /* Card Containers */
    .input-card, .output-card {
        background: linear-gradient(135deg, rgba(26,26,26,0.9) 0%, rgba(10,10,10,0.9) 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid var(--border-gray);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-white);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-gold);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input Fields - FIXED TEXT COLOR */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: rgba(0,0,0,0.4) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--accent-gold);
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
    }
    
    /* Placeholder text color */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-gray) !important;
        opacity: 0.6;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #B8941F 100%);
        color: var(--primary-black);
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
        background: linear-gradient(135deg, #E5C04A 0%, var(--accent-gold) 100%);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background-color: rgba(255,255,255,0.03);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--border-gray);
    }
    
    .stRadio > div > label {
        color: var(--text-gray);
        font-weight: 600;
    }
    
    .stRadio > div > div > label {
        color: var(--primary-white);
        transition: all 0.3s ease;
    }
    
    .stRadio > div > div > label:hover {
        color: var(--accent-gold);
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, rgba(212,175,55,0.1) 0%, rgba(212,175,55,0.05) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(212,175,55,0.3);
    }
    
    .stMetric > div > div {
        color: var(--primary-white);
    }
    
    .stMetric > div > div > div {
        color: var(--accent-gold);
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* JSON Display */
    .stJson {
        background-color: rgba(10,10,10,0.8);
        border: 1px solid var(--border-gray);
        border-radius: 10px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
    }
    
    /* Info/Warning/Success Boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        border-radius: 10px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1);
        border-left-color: #3B82F6;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: var(--warning-amber);
    }
    
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left-color: var(--success-green);
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left-color: var(--error-red);
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid var(--border-gray);
    }
    
    /* Confidence Badge */
    .confidence-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .confidence-high {
        background: linear-gradient(135deg, var(--success-green) 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, var(--warning-amber) 0%, #D97706 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    }
    
    .confidence-low {
        background: linear-gradient(135deg, var(--error-red) 0%, #DC2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Latency Indicator */
    .latency-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .latency-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #3B82F6;
    }
    
    /* Ambiguity List */
    .ambiguity-item {
        background: rgba(245, 158, 11, 0.05);
        border-left: 3px solid var(--warning-amber);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    /* Refinement Section */
    .refinement-section {
        background: linear-gradient(135deg, rgba(212,175,55,0.05) 0%, rgba(212,175,55,0.02) 100%);
        border: 2px dashed var(--accent-gold);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Logo Animation */
    @keyframes glow {
        0%, 100% {
            text-shadow: 2px 2px 20px rgba(212, 175, 55, 0.3);
        }
        50% {
            text-shadow: 2px 2px 30px rgba(212, 175, 55, 0.6);
        }
    }
    
    .magppie-logo {
        animation: glow 3s ease-in-out infinite;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-gold);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #E5C04A;
    }
    
    /* Selectbox Styling */
    .stSelectbox label {
        color: var(--accent-gold);
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Text Area Label */
    .stTextArea label, .stTextInput label {
        color: var(--accent-gold);
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Caption Styling */
    .stCaption {
        color: #FFFFFF !important;
    }
    
    /* Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.6rem 1.5rem;
        border: none;
        border-radius: 8px;
        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 18px rgba(59, 130, 246, 0.5);
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    }

    /* System Design Tab Styling */
    .sysdesign-card {
        background: linear-gradient(135deg, rgba(26,26,26,0.9) 0%, rgba(10,10,10,0.9) 100%);
        padding: 2.5rem;
        border-radius: 15px;
        border: 1px solid var(--border-gray);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 2rem;
    }

    .sysdesign-card h2 {
        color: var(--accent-gold);
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--accent-gold);
    }

    .sysdesign-card h3 {
        color: var(--primary-white);
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    .sysdesign-card p {
        color: #D0D0D0;
        line-height: 1.8;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .sysdesign-card ul {
        color: #D0D0D0;
        line-height: 1.8;
        padding-left: 1.5rem;
    }

    .sysdesign-card li {
        margin-bottom: 0.5rem;
    }

    .sysdesign-card li strong {
        color: var(--accent-gold);
    }

    .wordcount-badge {
        display: inline-block;
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid var(--accent-gold);
        color: var(--accent-gold);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# CUSTOM HEADER COMPONENT
# ============================================================================
def render_header():
    st.markdown("""
    <div class="magppie-header">
        <h1 class="magppie-logo">MAGPPIE</h1>
        <p class="magppie-tagline">AI KITCHEN DESIGN INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CONFIDENCE BADGE COMPONENT
# ============================================================================
def render_confidence_badge(confidence: float):
    if confidence >= 0.8:
        badge_class = "confidence-high"
        icon = "✅"
        label = "High Confidence"
    elif confidence >= 0.5:
        badge_class = "confidence-medium"
        icon = "⚠️"
        label = "Medium Confidence"
    else:
        badge_class = "confidence-low"
        icon = "❌"
        label = "Low Confidence"
    
    st.markdown(f"""
    <div class="confidence-badge {badge_class}">
        {icon} {label}: {confidence*100:.0f}%
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    load_css()
    render_header()
    
    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["✨ Assistant", "📜 Interaction History", "🧠 System Design"])
    
    # ========================================================================
    # TAB 1: DESIGN ASSISTANT
    # ========================================================================
    with tab1:
        col_in, col_out = st.columns([1, 1], gap="large")
        
        # --------------------------------------------------------------------
        # LEFT COLUMN: INPUT
        # --------------------------------------------------------------------
        with col_in:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🎤 Customer Input</div>', unsafe_allow_html=True)
            
            # Mode Selection
            mode = st.radio(
                "Input Mode:",
                ["💬 Text", "🎙️ Voice Prototype"],
                horizontal=True,
                key="mode_selector"
            )
            
            # Show note when Voice Prototype is selected
            if "Voice" in mode:
                st.warning("⚠️ **Note:** For this assessment, the STT (Speech-to-Text) layer is simulated to ensure cross-platform stability. In production, this would connect to a real-time Whisper or Gemini Multimodal endpoint.")
            
            # Prompt Version Toggle
            version_choice = st.selectbox(
                "🔧 Business Logic Version:",
                ["v1 (Standard Production)", "v2_strict (Luxury/Micro-Budget Flags)"],
                help="v2_strict adds additional budget-tier validations"
            )
            v_key = "v2_strict" if "v2" in version_choice else "v1"
            
            # Preset Test Cases
            preset_map = {
                "✍️ Manual Entry": "",
                "🧪 Case 1: Straight Kitchen (1.5L)": "Straight kitchen, all white, under 1.5 lakh, need a chimney",
                "🧪 Case 2: Elegant (Flexible)": "Something elegant, I don't know the layout, budget is flexible but not too high",
                "🧪 Case 3: U-shape (5-6L)": "U-shape, dark wood finish, island counter, around 5 to 6 lakh",
                "🧪 Case 4: Hinglish (3L)": "Bana do kuch achha, budget 3 lakh, white color"
            }
            
            selected_preset = st.selectbox(
                "📋 Quick Presets / Official Test Cases:",
                list(preset_map.keys())
            )
            final_val = preset_map[selected_preset]
            
            # Input Method Logic
            if "Voice" in mode:
                st.info("🎤 **Voice Simulation Active** - STT is simulated for assessment stability.")
                
                if st.button("🔴 Simulate Voice Recording", use_container_width=True):
                    st.session_state['voice_text'] = "Bana do kuch achha, budget 3 lakh, white color"
                    st.success("✅ Voice Captured and Transcribed!")
                
                simulated_text = st.session_state.get('voice_text', "")
                user_input = st.text_input("📝 Transcription:", value=simulated_text)
            else:
                user_input = st.text_area(
                    "📝 Customer Description:",
                    value=final_val,
                    height=150,
                    placeholder="Describe your dream kitchen..."
                )
            
            # Provider Selection
            provider = st.selectbox(
                "🤖 LLM Provider (Intelligence Engine):",
                ["Gemini 2.5 (Primary)", "Groq / Llama-3 (Fallback)"],
                help="Gemini 2.5 Flash for production, Groq for fallback"
            )
            
            # Extract Button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 EXTRACT DESIGN INTENT", use_container_width=True, type="primary"):
                if user_input.strip():
                    with st.spinner("🔍 Analyzing intent and checking guardrails..."):
                        start_time = time.time()
                        try:
                            result = extract_kitchen_intent(user_input, provider=provider, version=v_key)
                            latency = time.time() - start_time
                            
                            st.session_state['last_result'] = result
                            st.session_state['last_latency'] = latency
                            st.session_state['last_provider'] = provider
                            
                            # Success notification
                            st.success(f"✅ Intent extracted in {latency:.2f}s")
                        except Exception as e:
                            st.error(f"❌ System Error: {e}. Try switching providers.")
                else:
                    st.warning("⚠️ Please enter a description or select a preset.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --------------------------------------------------------------------
        # RIGHT COLUMN: OUTPUT
        # --------------------------------------------------------------------
        with col_out:
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Structured Design Data</div>', unsafe_allow_html=True)
            
            if 'last_result' in st.session_state:
                res = st.session_state['last_result']
                lat = st.session_state.get('last_latency', 0)
                prov = st.session_state.get('last_provider', "Unknown")
                
                # Confidence Badge
                render_confidence_badge(res.confidence)
                
                # Metrics Row
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(
                        "⚡ Latency",
                        f"{lat:.2f}s",
                        delta=f"{prov.split('/')[0].strip()}"
                    )
                with metric_col2:
                    st.metric(
                        "🎯 Confidence Score",
                        f"{res.confidence*100:.1f}%",
                        delta="Ready" if res.confidence > 0.8 else "Needs Review"
                    )
                
                # JSON Output
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**📄 Extracted JSON:**")
                st.json(res.model_dump())
                
                # Download Button for JSON
                json_str = json.dumps(res.model_dump(), indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name="magppie_design_intent.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                # Ambiguities Section
                if res.ambiguities:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.warning("⚠️ **Showroom Notes / Ambiguities:**")
                    for amb in res.ambiguities:
                        st.markdown(f'<div class="ambiguity-item">• {amb}</div>', unsafe_allow_html=True)
                    
                    # Refinement UI
                    if res.confidence < 0.85:
                        st.markdown('<div class="refinement-section">', unsafe_allow_html=True)
                        st.markdown("### 💡 Clarify Your Design")
                        st.caption("Add missing details to improve extraction accuracy")
                        
                        refinement = st.text_input(
                            "Additional Details:",
                            placeholder="e.g., 'I prefer L-shape layout' or 'Budget max 5 lakh'"
                        )
                        
                        if st.button("🔄 UPDATE DESIGN INTENT", use_container_width=True):
                            if refinement:
                                enriched_input = f"{user_input}. Clarification: {refinement}"
                                with st.spinner("🔄 Refining extraction..."):
                                    new_result = extract_kitchen_intent(enriched_input, provider=provider, version=v_key)
                                    st.session_state['last_result'] = new_result
                                    st.rerun()
                            else:
                                st.warning("Please provide clarification details")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                elif res.confidence > 0.9:
                    st.success("✅ **Clean Extraction: Ready for Design Engine**")
            else:
                # Placeholder when no results
                st.info("👈 Enter customer input and click **Extract** to see results")
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: var(--text-gray);">
                    <h3>Awaiting Input</h3>
                    <p>The AI is ready to analyze your kitchen design requirements</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 2: INTERACTION HISTORY
    # ========================================================================
    with tab2:
        st.markdown('<div class="section-header">📜 Showroom Interaction Logs</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: white; font-size: 0.875rem; margin-bottom: 1rem;">Real-time persistent history of all design extractions</p>', unsafe_allow_html=True)
        
        history = load_history()
        if history:
            # Reverse to show latest first
            st.dataframe(
                history[::-1],
                use_container_width=True,
                height=600
            )
            
            # Download option
            st.download_button(
                "📥 Download History (JSON)",
                data=str(history),
                file_name="magppie_extraction_history.json",
                mime="application/json"
            )
        else:
            st.info("📭 No interactions recorded yet. Process an input to see logs.")

    # ========================================================================
    # TAB 3: SYSTEM DESIGN
    # ========================================================================
    with tab3:
        st.markdown('<div class="section-header">🧠 Task 02: System Thinking & Scalability</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="sysdesign-card">
            <h2>1. Data Collection &amp; The Improvement Flywheel</h2>
            <p>
                Our pipeline logs every interaction: raw input, provider, JSON output, confidence, and latency.
                To close the feedback loop, I'd enrich this with three high-signal data points:
                <strong style="color: #D4AF37;">Showroom Outcome</strong> (design approval),
                <strong style="color: #D4AF37;">Consultant Correction</strong> (human overrides), and
                <strong style="color: #D4AF37;">User Refinement</strong> (captured via the built-in refinement interface).
            </p>
            <p>
                This creates a high-fidelity 'Gold Standard' dataset. Low-confidence extractions that lead to approvals
                reveal prompt blind spots, while high-confidence extractions requiring human correction expose hallucination
                patterns. I'd use LangSmith (already integrated via <code style="color: #D4AF37; background: rgba(212,175,55,0.1); padding: 0.1rem 0.4rem; border-radius: 4px;">@traceable</code>)
                to cluster failures by type (e.g., Hinglish misparses), turning each cluster into a targeted test case
                for our automated regression suite.
            </p>
        </div>

        <div class="sysdesign-card">
            <h2>2. Detecting Model Degradation</h2>
            <p>I would monitor four key signals via a real-time dashboard:</p>
            <ul>
                <li>
                    <strong>Confidence Distribution Shift:</strong>
                    A drop in average confidence despite stable input complexity indicates model drift or API behavior changes.
                </li>
                <li>
                    <strong>Ambiguity Rate Spike:</strong>
                    A rise in <code style="color: #D4AF37; background: rgba(212,175,55,0.1); padding: 0.1rem 0.4rem; border-radius: 4px;">ambiguities</code>
                    suggests the model is losing decisiveness on evolving customer slang.
                </li>
                <li>
                    <strong>Semantic Drift:</strong>
                    Monitoring embedding distances between inputs and outputs; if similar intents produce divergent JSON,
                    the prompt has regressed.
                </li>
                <li>
                    <strong>The 'Ground Truth' Gap:</strong>
                    If extraction confidence stays high but showroom design approvals drop, the model is technically
                    correct but failing to capture true customer intent.
                </li>
            </ul>
            <div class="wordcount-badge">📝 Word Count: 238</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    main()