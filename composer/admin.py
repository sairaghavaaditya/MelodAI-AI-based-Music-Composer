from django.contrib import admin
from .models import Composition


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "genre", "tempo_bpm", "length_seconds", "created_at")
    list_filter = ("genre", "model_used", "created_at")
    search_fields = ("title", "owner__username", "mood", "instruments")

# Register your models here.
