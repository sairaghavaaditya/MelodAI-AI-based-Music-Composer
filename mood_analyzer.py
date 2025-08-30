from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
from scipy.special import softmax # Import softmax from scipy
from config import Config # Assuming config.py is in the same directory
from music_parameters import *
class MoodAnalyzer:
    """
    Analyzes user input text to determine mood, sentiment, and energy level,
    then maps these to musical parameters.
    """
    def __init__(self):
        """
        Initializes sentiment analysis model, embedding model,
        and pre-computes embeddings for mood categories.
        """
        print(f"Loading sentiment model: {Config.SENTIMENT_MODEL} to {Config.DEVICE}")
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(Config.SENTIMENT_MODEL)
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(Config.SENTIMENT_MODEL)
        self.sentiment_model.to(Config.DEVICE) # Move model to specified device
        self.sentiment_model.eval() # Set model to evaluation mode

        print(f"Loading embedding model: {Config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.embedding_model.to(Config.DEVICE) # Move model to specified device
        self.embedding_model.eval() # Set model to evaluation mode

        # Define mood categories and pre-compute their embeddings
        self.mood_categories = {
            "happy": "joyful, cheerful, ecstatic, delighted",
            "sad": "depressed, sorrowful, melancholic, gloomy",
            "calm": "peaceful, tranquil, serene, relaxed",
            "energetic": "vibrant, lively, enthusiastic, active",
            "mysterious": "enigmatic, strange, secretive, suspenseful",
            "romantic": "loving, passionate, intimate, tender"
        }
        self.mood_embeddings = self._precompute_mood_embeddings()
        print("Now you can start generate music...")

        # Energy level keywords (simple approach)
        self.high_energy_words = ["excited", "energetic", "thrilled", "fast", "upbeat", "workout", "lively", "vibrant", "dynamic", "intense"]
        self.low_energy_words = ["calm", "relaxed", "sleepy", "slow", "peaceful", "quiet", "mellow", "tranquil", "chill", "soft"]

    def _precompute_mood_embeddings(self):
        """
        Generates embeddings for defined mood categories.
        """
        print("Pre-computing mood embeddings...")
        mood_sentences = [self.mood_categories[m] for m in self.mood_categories]
        # Encode sentences in batches for efficiency
        with torch.no_grad():
            embeddings = self.embedding_model.encode(mood_sentences, convert_to_tensor=True, device=Config.DEVICE)
        return {mood: embeddings[i] for i, mood in enumerate(self.mood_categories.keys())}

    def _get_sentiment(self, text):
        """
        Determines the sentiment (positive, neutral, negative) of the text.
        Returns sentiment label and confidence score.
        """
        encoded_input = self.sentiment_tokenizer(text, return_tensors='pt', max_length=Config.MAX_LENGTH, truncation=True).to(Config.DEVICE)
        with torch.no_grad():
            output = self.sentiment_model(**encoded_input)
        scores = output.logits[0].cpu().numpy()
        scores = softmax(scores) # Apply softmax to get probabilities

        # Sentiment labels for roberta-base-sentiment-latest:
        # 0: negative, 1: neutral, 2: positive
        labels = ['negative', 'neutral', 'positive']
        sentiment_id = np.argmax(scores)
        sentiment_label = labels[sentiment_id]
        confidence = scores[sentiment_id]
        return sentiment_label, confidence

    def _get_mood_category(self, text):
        """
        Classifies the text into one of the predefined mood categories
        using cosine similarity with pre-computed embeddings.
        """
        with torch.no_grad():
            user_embedding = self.embedding_model.encode(text, convert_to_tensor=True, device=Config.DEVICE)

        similarities = {}
        for mood, mood_embedding in self.mood_embeddings.items():
            similarity = util.cos_sim(user_embedding, mood_embedding)
            similarities[mood] = similarity.item() # .item() to get scalar from tensor

        closest_mood = max(similarities, key=similarities.get)
        return closest_mood, similarities[closest_mood]

    def _calculate_energy_level(self, text, sentiment):
        """
        Calculates an energy level (1-10) based on keywords and sentiment.
        """
        text_lower = text.lower()
        high_energy_count = sum(1 for word in self.high_energy_words if word in text_lower)
        low_energy_count = sum(1 for word in self.low_energy_words if word in text_lower)

        base_energy = 5 # Start with a neutral energy

        # Adjust base energy based on sentiment
        if sentiment == 'positive':
            base_energy += 2
        elif sentiment == 'negative':
            base_energy -= 1 # Sad can still have some energy, but less

        # Adjust based on keyword counts
        energy_from_keywords = (high_energy_count * 2) - (low_energy_count * 1)
        final_energy = base_energy + energy_from_keywords

        # Clamp the energy level between 1 and 10
        final_energy = max(1, min(10, final_energy))
        return final_energy

    def analyze(self, user_text):
        """
        Main analysis function to process user text and return musical parameters.
        """
        sentiment_label, sentiment_confidence = self._get_sentiment(user_text)
        mood_category, mood_similarity = self._get_mood_category(user_text)
        energy_level = self._calculate_energy_level(user_text, sentiment_label)

        # Map to musical parameters
        musical_params = get_musical_parameters(mood_category, sentiment_label, energy_level)

        return {
            "user_text": user_text,
            "sentiment": {"label": sentiment_label, "confidence": f"{sentiment_confidence:.2f}"},
            "mood": {"category": mood_category, "similarity": f"{mood_similarity:.2f}"},
            "energy_level": energy_level,
            "musical_parameters": musical_params
        }