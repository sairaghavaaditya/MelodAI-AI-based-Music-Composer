from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Composition(models.Model):
    GENRE_CHOICES = [
        ("classical", "Classical"),
        ("jazz", "Jazz"),
        ("pop", "Pop"),
        ("rock", "Rock"),
        ("ambient", "Ambient"),
        ("electronic", "Electronic"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compositions")
    title = models.CharField(max_length=255)
    mood = models.CharField(max_length=64, blank=True)
    genre = models.CharField(max_length=32, choices=GENRE_CHOICES, default="ambient")
    instruments = models.CharField(max_length=255, blank=True, help_text="Comma-separated instruments")
    tempo_bpm = models.PositiveIntegerField(default=120)
    length_seconds = models.PositiveIntegerField(default=30)
    model_used = models.CharField(max_length=255, default="stub-generator")
    audio_file = models.FileField(upload_to="compositions/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # noqa: D401
        return f"{self.title} ({self.owner})"

# Create your models here.
