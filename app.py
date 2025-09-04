# app.py

import streamlit as st
import time
import os
from mood_analyzer import MoodAnalyzer
from music_parameters import get_musical_parameters
from music_generator import MusicGenerator

# --- Corrected placement ---
st.set_page_config(
    page_title="MelodAI: AI-based Music Composer",
    page_icon="🎶",
    layout="centered"
)
# --- End of corrected placement ---

# Initialize the MoodAnalyzer and MusicGenerator.
# Using st.cache_resource to avoid re-loading models every time the script reruns.
@st.cache_resource
def load_models():
    """Loads and caches the MoodAnalyzer and MusicGenerator instances."""
    return MoodAnalyzer(), MusicGenerator()

analyzer, generator = load_models()

# A cache for the analysis results to prevent re-running on every change
@st.cache_data
def analyze_text_with_cache(text):
    """
    Analyzes the text and caches the result based on the text input.
    This function will re-run only when the `text` argument changes.
    """
    return analyzer.analyze(text)


# --- Streamlit UI Setup ---
st.markdown(
    """
    <style>
    .main {
        background-color: #00000;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTextInput label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stAlert {
        border-radius: 8px;
    }
    .stProgress .st-bc {
        height: 10px;
        border-radius: 5px;
    }
    .parameter-box {
        background-color: #e6f7ff;
        border-left: 5px solid #007bff;
        padding: 15px;
        margin-top: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .parameter-box h3 {
        color: #007bff;
        margin-bottom: 10px;
    }
    .parameter-item {
        margin-bottom: 5px;
    }
    .parameter-item strong {
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎶 MelodAI: AI-based Music Composer")
st.markdown(
    "Enter a description of your mood, context, or situation, and MelodAI will create a short musical piece for you!"
)

# User input text area
user_input = st.text_area(
    "Tell me about your mood or what kind of music you need:",
    placeholder="e.g., 'I'm feeling happy and energetic, ready for a workout!' or 'I need calm, peaceful music for studying.'",
    height=100
)

# Generate Music button
if st.button("Generate Music"):
    if user_input:
        # Step 1: Analyze Mood
        with st.spinner("Analyzing your mood and generating parameters..."):
            # Use the cache-based function
            mood_analysis_result = analyze_text_with_cache(user_input)
            
            if mood_analysis_result:
                # Correctly extract the string values from the nested dictionaries
                mood_string = mood_analysis_result.get("mood_classification", "calm")
                sentiment_string = mood_analysis_result.get("sentiment", {}).get("label", "neutral")
                energy_int = mood_analysis_result.get("energy_level", 5)

                # Pass the extracted values to the function
                musical_params = get_musical_parameters(
                    mood_string,
                    sentiment_string,
                    energy_int
                )
            else:
                st.error("Mood analysis failed. Please try again.")
                musical_params = None

        if musical_params:
            st.success("Mood analysis complete!")
            st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
            st.markdown(f"<h3>Suggested Music Profile</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Mood Classification:</strong> {musical_params.get('mood', 'N/A').capitalize()}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Sentiment:</strong> {musical_params.get('sentiment', 'N/A').capitalize()}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Energy Level:</strong> {musical_params.get('energy', 'N/A')}/10</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Tempo (BPM):</strong> {musical_params.get('tempo', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Key:</strong> {musical_params.get('key', 'N/A').capitalize()}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='parameter-item'><strong>Instruments:</strong> {', '.join([i.capitalize() for i in musical_params.get('instruments', ['N/A'])])}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Step 2: Generate Music
            with st.spinner("Generating music... This may take a moment."):
                audio_path = generator.generate_music(musical_params)
                
            if audio_path and os.path.exists(audio_path):
                st.success("Music generation complete! Play your custom track below.")
                st.audio(audio_path, format="audio/wav")
                os.remove(audio_path) # Clean up the generated file

            else:
                st.error("Failed to generate music. Please check the logs for details.")

    else:
        st.warning("Please enter some text to analyze your mood.")

st.markdown("---")
st.markdown("Powered by Hugging Face 🤗 and Streamlit 🚀")