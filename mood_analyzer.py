# mood_analyzer.py

import torch
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

class MoodAnalyzer:
    """
    Analyzes user text to determine mood, sentiment, and energy level,
    and maps these to musical parameters.
    """
    def __init__(self):
        """Initializes the models and pre-computes mood embeddings."""
        self.sentiment_model = None
        self.sentiment_tokenizer = None
        self.embedding_model = None
        self.mood_embeddings = None
        self.mood_categories = ["happy", "sad", "calm", "energetic", "mysterious", "romantic"]
        self.device = Config.DEVICE

        self._load_models()
        self._precompute_mood_embeddings()

    def _load_models(self):
        """Loads the Hugging Face models for sentiment analysis and embeddings."""
        try:
            print(f"Loading sentiment model: {Config.SENTIMENT_MODEL} to {self.device}")
            self.sentiment_tokenizer = AutoTokenizer.from_pretrained(Config.SENTIMENT_MODEL)
            self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(Config.SENTIMENT_MODEL)
            self.sentiment_model.to(self.device)

            print(f"Loading embedding model: {Config.EMBEDDING_MODEL}")
            self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            self.embedding_model.to(self.device)

        except Exception as e:
            print(f"Error loading models: {e}")
            self.sentiment_model = None
            self.embedding_model = None

    def _precompute_mood_embeddings(self):
        """Creates and stores vector embeddings for the mood categories."""
        if not self.embedding_model:
            print("Embedding model not loaded. Cannot pre-compute embeddings.")
            return

        print("Pre-computing mood embeddings...")
        self.mood_embeddings = self.embedding_model.encode(self.mood_categories)

    def _get_sentiment(self, text: str) -> dict:
        """Analyzes text sentiment (positive, negative, neutral)."""
        if not self.sentiment_model or not self.sentiment_tokenizer:
            return {"label": "neutral", "score": 0.5}

        encoded_text = self.sentiment_tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        encoded_text.to(self.device)
        output = self.sentiment_model(**encoded_text)
        scores = torch.softmax(output.logits, dim=1).squeeze().tolist()
        
        # Get the label with the highest score
        labels = ["negative", "neutral", "positive"]
        sentiment_label = labels[scores.index(max(scores))]
        sentiment_score = max(scores)

        return {"label": sentiment_label, "score": sentiment_score}

    def _classify_mood(self, text: str) -> str:
        """Finds the closest mood category based on text similarity."""
        if not self.embedding_model or self.mood_embeddings is None:
            return "calm"

        user_embedding = self.embedding_model.encode([text])[0]
        
        # Reshape for cosine similarity calculation
        user_embedding = user_embedding.reshape(1, -1)
        
        # Calculate cosine similarity between the user text and mood categories
        similarities = cosine_similarity(user_embedding, self.mood_embeddings)[0]
        
        # Find the index of the highest similarity score
        best_mood_index = np.argmax(similarities)
        
        # Print for debugging
        print(f"Calculated similarities: {similarities}")
        print(f"Closest mood: {self.mood_categories[best_mood_index]}")

        return self.mood_categories[best_mood_index]

    def _calculate_energy_level(self, text: str, sentiment: str) -> int:
        """Calculates an energy level from 1-10 based on keywords and sentiment."""
        high_energy_words = ["energetic", "upbeat", "fast", "powerful", "excited", "happy", "joyful", "party"]
        low_energy_words = ["calm", "slow", "peaceful", "sad", "sleepy", "down", "quiet", "serene"]

        energy_score = 5 # Start at a neutral value
        
        # Adjust based on sentiment
        if sentiment == "positive":
            energy_score += 2
        elif sentiment == "negative":
            energy_score -= 2

        # Adjust based on keywords
        text_lower = text.lower()
        for word in high_energy_words:
            if word in text_lower:
                energy_score += 1
        for word in low_energy_words:
            if word in text_lower:
                energy_score -= 1
        
        # Clamp the score to a 1-10 range
        energy_score = max(1, min(10, energy_score))
        
        # Print for debugging
        print(f"Calculated energy level: {energy_score}")
        
        return energy_score

    def analyze(self, text: str) -> dict:
        """Main analysis function to get all musical parameters."""
        if not self.sentiment_model or not self.embedding_model:
            print("Models not loaded, cannot perform analysis.")
            return None

        sentiment = self._get_sentiment(text)
        mood_classification = self._classify_mood(text)
        energy_level = self._calculate_energy_level(text, sentiment["label"])
        
        return {
            "mood_classification": mood_classification,
            "sentiment": sentiment,
            "energy_level": energy_level
        }

