import torch

class Config:
    """
    Configuration settings for the MelodAI project.
    Defines model names, maximum sequence length, and device for computation.
    """
    SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_LENGTH = 128
    # Automatically set device to 'cuda' if a GPU is available, otherwise 'cpu'
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"