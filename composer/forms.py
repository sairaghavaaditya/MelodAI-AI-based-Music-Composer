from django import forms
from .models import Composition


class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = [
            "title",
            "mood",
            "genre",
            "instruments",
            "tempo_bpm",
            "length_seconds",
        ]

    def clean_tempo_bpm(self):
        tempo = self.cleaned_data.get("tempo_bpm")
        if tempo and (tempo < 40 or tempo > 240):
            raise forms.ValidationError("Tempo must be between 40 and 240 BPM.")
        return tempo

    def clean_length_seconds(self):
        length = self.cleaned_data.get("length_seconds")
        if length and (length < 5 or length > 300):
            raise forms.ValidationError("Length must be between 5 and 300 seconds.")
        return length


