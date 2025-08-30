def get_musical_parameters(mood, sentiment, energy_level):
    """
    Maps mood, sentiment, and energy level to musical parameters.

    Args:
        mood (str): The classified mood (e.g., "happy", "sad", "calm").
        sentiment (str): The sentiment of the text (e.g., "positive", "negative", "neutral").
        energy_level (int): Energy level on a scale of 1-10.

    Returns:
        dict: A dictionary of musical parameters.
    """
    # Base tempos for moods
    base_tempos = {
        "happy": 120,
        "energetic": 140,
        "calm": 80,
        "sad": 60,
        "mysterious": 90,
        "romantic": 75
    }

    # Base keys for sentiments
    base_keys = {
        "positive": "major",
        "negative": "minor",
        "neutral": "major" # Default to major for neutral
    }

    # Instrument suggestions based on mood
    instrument_suggestions = {
        "happy": ["piano", "guitar", "drums", "strings"],
        "energetic": ["drums", "synth", "electric guitar", "bass"],
        "calm": ["piano", "flute", "strings", "acoustic guitar"],
        "sad": ["cello", "strings", "piano", "oboe"],
        "mysterious": ["strings (pizzicato)", "low brass", "synthesizer pads", "percussion"],
        "romantic": ["piano", "strings", "saxophone", "harp"]
    }

    # Adjust tempo based on energy level
    # Energy level 1-10, scale factor -0.25 to +0.25 (total range 0.5)
    # Mid-point (5.5) means no change
    tempo_adjustment_factor = ((energy_level - 5.5) / 10) * 0.5

    tempo = int(base_tempos.get(mood, 100) * (1 + tempo_adjustment_factor))
    # Ensure tempo is within a reasonable range
    tempo = max(40, min(200, tempo))

    key = base_keys.get(sentiment, "major")
    instruments = instrument_suggestions.get(mood, ["piano", "strings"])

    return {
        "tempo": tempo,
        "key": key,
        "mood": mood,
        "energy": energy_level,
        "instruments": instruments
    }