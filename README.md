# 🎶 MelodAI: AI-based Music Composer

[![Status](https://img.shields.io/badge/Status-Milestone%201%20Completed-brightgreen)](https://github.com/Springboard-Internship-2025/Development-of-an-AI-Based-Music-Composition-System_August_2025)

## ✨ Project Overview

**MelodAI** is an intelligent music composition system designed to generate personalized musical parameters. It takes user-defined moods, contexts, or situations as input and leverages cutting-edge AI models to create musical suggestions that align with their emotions or scenarios. The goal is to provide an intuitive and seamless experience for effortlessly creating custom music.

This repository currently reflects the completion of **Milestone 1: Core Foundation & Mood Analysis**.

## 🚀 Milestone 1: Core Functionality - Mood to Music Parameters

In this first milestone, MelodAI focuses on the intelligent interpretation of textual user input and its translation into foundational musical attributes. We've built the "brain" that understands your feelings and translates them into musical language.

### 🧠 Technical Approach & Models Used

The core of Milestone 1 involves a sophisticated NLP pipeline:

1.  **User Text Input:** The system receives a textual description of a mood or context (e.g., "I'm feeling incredibly joyful and ready to conquer the day!").
2.  **Sentiment Analysis:**
    * **Model:** Hugging Face `transformers` with `cardiffnlp/twitter-roberta-base-sentiment-latest`.
    * **Approach:** This model processes the text to determine its overall emotional polarity (positive, negative, or neutral) and provides a confidence score.
3.  **Mood Classification:**
    * **Model:** Sentence-Transformers with `all-MiniLM-L6-v2`.
    * **Approach:** The user's input text is converted into a numerical vector (a "sentence embedding"). This embedding is then compared using **cosine similarity** against pre-computed embeddings of six predefined mood categories (Happy, Sad, Calm, Energetic, Mysterious, Romantic) to find the closest emotional match.
4.  **Energy Level Calculation:**
    * **Approach:** A heuristic-based system that scans the input text for high-energy and low-energy keywords, combining this with the detected sentiment to estimate an overall energy level on a scale of 1-10.
5.  **Musical Parameter Mapping:**
    * **Approach:** The derived mood, sentiment, and energy level are translated into concrete musical parameters using a set of predefined rules. This involves suggesting:
        * **Tempo (BPM):** Dynamically adjusted based on mood and energy (e.g., Happy + high energy = faster tempo).
        * **Musical Key:** `Major` for positive/neutral sentiment, `Minor` for negative sentiment.
        * **Instruments:** A list of instruments commonly associated with the detected mood (e.g., Piano, Guitar, Drums for Happy; Cello, Strings for Sad).

## 📊 How It Works (Workflow)

The application follows a clear data flow from user input to musical output:

1.  **Start Application (`app.py`):** The Streamlit web application launches, loads, and caches the necessary AI models (`MoodAnalyzer`).
2.  **User Input:** You describe your mood/context in a text input field.
3.  **Trigger Analysis:** You click "Generate Music Parameters."
4.  **Text Analysis (`mood_analyzer.py`):**
    * Your text goes through the sentiment model.
    * Your text is converted into an embedding and compared for mood classification.
    * Keywords are analyzed for energy level.
5.  **Parameter Generation (`music_parameters.py`):** The analyzed mood, sentiment, and energy are mapped to specific tempo, key, and instrument suggestions.
6.  **Display Results (`app.py`):** The suggested musical parameters are displayed on the web interface in a clear, organized format.

## 📁 Project Structure

```
AI_music_composition/
├── app.py                  # Main Streamlit web application for the UI and orchestration.
├── mood_analyzer.py        # Core AI engine for text analysis (sentiment, mood, energy).
├── music_parameters.py     # Defines the mapping logic from analysis results to musical parameters.
├── config.py               # Centralized configuration settings (model names, device).
├── requirements.txt        # Lists all Python dependencies required for the project.
└── README.md               # This file!
```

## 🛠️ Setup and Local Run

Follow these steps to get MelodAI up and running on your local machine:

### Prerequisites

* Python 3.10
* Conda (recommended for environment management) or `pip`

### 1. Clone the Repository

```bash
git clone [https://github.com/Springboard-Internship-2025/Development-of-an-AI-Based-Music-Composition-System_August_2025.git](https://github.com/Springboard-Internship-2025/Development-of-an-AI-Based-Music-Composition-System_August_2025.git)
cd Development-of-an-AI-Based-Music-Composition-System_August_2025
```

### 2. Create and Activate Conda Environment (Recommended)

```bash
conda create -n melodAI-env python=3.10
conda activate melodAI-env
```
*(If you prefer `pip` without Conda, skip this step and directly install requirements.)*

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
The `requirements.txt` file contains:
```
streamlit==1.28.0
transformers==4.35.0
torch==2.1.0
sentence-transformers==2.2.2
numpy==1.25.0
pandas==2.1.0
scikit-learn==1.3.0
scipy==1.11.4
```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

This command will open the MelodAI web application in your default web browser (usually at `http://localhost:8501`).

## 👨‍💻 Usage

1.  **Launch the App:** Run `streamlit run app.py` as described above.
2.  **Enter Text:** In the "Describe your mood or context:" text box, type how you're feeling or the situation you're in.
    * *Examples:* "I need calm music for studying", "Feeling excited for a party", "Something mysterious for a rainy evening."
3.  **Generate Parameters:** Click the "Generate Music Parameters" button.
4.  **View Results:** The application will display the detected mood, sentiment, energy level, and the suggested musical parameters (tempo, key, instruments).

*(Note: The first time you run the app, it will download and load large AI models, which might take a few minutes depending on your internet speed and system. Please be patient until the "Loading AI models..." spinner disappears.)*

## 💡 Future Enhancements

This project is a foundation. Future work will include:

* Integration with actual music generation libraries (e.g., `music21`, `pretty_midi`, or deep learning music models) to compose playable audio/MIDI files based on the generated parameters.
* More sophisticated energy detection and mood refinement.
* User feedback loops for model improvement.

---

Made with ❤️ by Aditya
