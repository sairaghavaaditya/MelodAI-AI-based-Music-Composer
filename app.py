import streamlit as st
from mood_analyzer import MoodAnalyzer # Assuming mood_analyzer.py is in the same directory
import os

# Set page configuration for better aesthetics
st.set_page_config(layout="centered", page_title="MelodAI: AI Music Composer", page_icon="🎶")

# Custom CSS for a modern, rounded, and visually appealing look
st.markdown("""
<style>
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 30px;
        background-color: #1a1a2e; /* Dark blue-purple background */
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        color: #e0e0e0; /* Light gray text */
    }
    h1, h2, h3 {
        color: #e94560; /* Vibrant red-pink for titles */
        text-align: center;
        margin-bottom: 25px;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #2e3a51; /* Slightly lighter dark blue */
        color: #e0e0e0;
        border: 2px solid #5a5a72; /* Border color */
        border-radius: 10px;
        padding: 12px 15px;
        font-size: 16px;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #e94560; /* Highlight on focus */
        box-shadow: 0 0 0 0.2rem rgba(233, 69, 96, 0.25);
    }
    .stButton>button {
        width: 100%;
        background-color: #e94560; /* Button background */
        color: white;
        font-weight: bold;
        padding: 12px 20px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
    }
    .stButton>button:hover {
        background-color: #c93b51; /* Darker on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.6);
    }
    .stAlert {
        border-radius: 10px;
        background-color: #2e3a51;
        color: #e0e0e0;
        border: 1px solid #5a5a72;
    }
    .parameter-box {
        background-color: #2e3a51;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #5a5a72;
    }
    .parameter-box strong {
        color: #a7d9e7; /* Light blue for labels */
    }
    .loading-indicator {
        text-align: center;
        margin-top: 20px;
        color: #a7d9e7;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎶 MelodAI: AI Music Composer")
st.markdown("---")

st.markdown("""
<div class="main-container">
    <h3>Craft music based on your mood or context!</h3>
    <p style="text-align: center; color: #b0b0b0;">
        Enter a description of how you're feeling, or the situation you're in,
        and MelodAI will suggest musical parameters.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize MoodAnalyzer (this might take a moment the first time as models load)
@st.cache_resource
def load_mood_analyzer():
    """Caches the MoodAnalyzer instance to avoid re-loading models."""
    return MoodAnalyzer()

# Display a loading spinner while models are loading
with st.spinner('Loading AI models... This might take a moment.'):
    analyzer = load_mood_analyzer()

user_input = st.text_input(
    "Describe your mood or context:",
    placeholder="e.g., I'm feeling happy and energetic, ready for a workout!",
    key="user_text_input"
)

if st.button("Generate Music Parameters"):
    if user_input:
        with st.spinner("Analyzing your input and generating parameters..."):
            analysis_results = analyzer.analyze(user_input)

        st.subheader("Analysis Results:")
        # Display analysis results with custom styling
        st.markdown(f"""
        <div class="parameter-box">
            <strong>Original Input:</strong> {analysis_results['user_text']}<br>
            <strong>Detected Mood:</strong> {analysis_results['mood']['category']} (Similarity: {analysis_results['mood']['similarity']})<br>
            <strong>Detected Sentiment:</strong> {analysis_results['sentiment']['label']} (Confidence: {analysis_results['sentiment']['confidence']})<br>
            <strong>Calculated Energy Level:</strong> {analysis_results['energy_level']}/10
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Suggested Musical Parameters:")
        # Display musical parameters with custom styling
        musical_params = analysis_results['musical_parameters']
        st.markdown(f"""
        <div class="parameter-box">
            <strong>Tempo (BPM):</strong> {musical_params['tempo']}<br>
            <strong>Key:</strong> {musical_params['key'].capitalize()}<br>
            <strong>Instruments:</strong> {', '.join([i.capitalize() for i in musical_params['instruments']])}<br>
            <strong>Overall Mood:</strong> {musical_params['mood'].capitalize()}<br>
            <strong>Derived Energy:</strong> {musical_params['energy']}/10
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 These are suggested parameters. In future steps, we'll use these to actually compose music!")
    else:
        st.warning("Please enter some text to describe your mood or context.")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #5a5a72;'>Made with ❤️ by Aditya</p>",
    unsafe_allow_html=True
)
