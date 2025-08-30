# music_generator.py

import torch
import scipy.io.wavfile
from transformers import pipeline, AutoProcessor, MusicgenForConditionalGeneration
import traceback

class MusicGenerator:
    """
    A class to generate a musical piece based on a text prompt using a
    Hugging Face text-to-audio model.
    """
    def __init__(self, model_name="facebook/musicgen-small"):
        """
        Initializes the music generation pipeline.

        Args:
            model_name (str): The name of the Hugging Face music generation model.
        """
        self.model_name = model_name
        self.model = None
        self.processor = None
        self.device = torch.device("cpu")
        self._load_model()

    def _load_model(self):
        """Loads the text-to-audio model and processor."""
        try:
            print(f"Loading music generation model '{self.model_name}'...")
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.model = MusicgenForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)
            print("Music generation model loaded successfully.")
        except Exception as e:
            print(f"Error loading music generation model: {e}")
            traceback.print_exc()
            self.model = None
            self.processor = None

    def generate_music(self, musical_parameters: dict, duration_seconds: int = 15) -> str:
        """
        Generates music from a dictionary of musical parameters.

        Args:
            musical_parameters (dict): A dictionary of parameters from the mood analysis.
            duration_seconds (int): The desired duration of the generated music in seconds.

        Returns:
            str: The filepath to the generated WAV file, or None if generation fails.
        """
        if not self.model or not self.processor:
            print("Music generation model is not initialized.")
            return None

        # --- Step 1: Convert parameters to a descriptive text prompt ---
        mood = musical_parameters.get("mood", "calm")
        key = musical_parameters.get("key", "major")
        tempo = musical_parameters.get("tempo", 100)
        instruments = ", ".join(musical_parameters.get("instruments", ["piano", "strings"]))

        prompt = (
            f"A {mood} instrumental track in a {key} key. "
            f"The tempo is approximately {tempo} BPM. "
            f"It features the following instruments: {instruments}."
        )

        print(f"Generating music with prompt: '{prompt}'")

        try:
            # --- Step 2: Generate the audio using the model's direct generate method ---
            # This is more robust than using the pipeline's default parameters.
            inputs = self.processor(
                text=[prompt],
                return_tensors="pt"
            ).to(self.device)

            # Generate audio. Setting a shorter max_new_tokens for faster results.
            # 256 tokens roughly corresponds to 5 seconds of audio.
            audio_values = self.model.generate(**inputs, max_new_tokens=256)

            # --- Step 3: Save the audio to a WAV file ---
            sampling_rate = self.model.config.audio_encoder.sampling_rate
            output_path = "generated_music.wav"
            scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
            print(f"Music saved to {output_path}")

            return output_path
        except Exception as e:
            print(f"Error during music generation: {e}")
            traceback.print_exc()
            return None

