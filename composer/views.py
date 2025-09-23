from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, DetailView, ListView, View

from .forms import CompositionForm
from .models import Composition
from . import generator


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "composer/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CompositionForm()
        return context


class ComposeView(LoginRequiredMixin, FormView):
    template_name = "composer/home.html"
    form_class = CompositionForm

    def form_valid(self, form):
        composition: Composition = generator.generate_audio(
            owner=self.request.user,
            **form.cleaned_data,
        )
        return redirect(reverse("composer:result", args=[composition.pk]))


class ResultView(LoginRequiredMixin, DetailView):
    model = Composition
    template_name = "composer/result.html"
    context_object_name = "composition"

    def get_queryset(self):
        return Composition.objects.filter(owner=self.request.user)


class HistoryView(LoginRequiredMixin, ListView):
    model = Composition
    template_name = "composer/history.html"
    context_object_name = "compositions"

    def get_queryset(self):
        return Composition.objects.filter(owner=self.request.user)


class DownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        composition = get_object_or_404(Composition, pk=pk, owner=request.user)
        if not composition.audio_file:
            raise Http404("No file available")
        return FileResponse(composition.audio_file.open("rb"), as_attachment=True, filename=composition.audio_file.name.split("/")[-1])

# Create your views here.
