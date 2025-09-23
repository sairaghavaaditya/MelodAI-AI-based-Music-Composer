from django.urls import path
from . import views


app_name = "composer"


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("compose/", views.ComposeView.as_view(), name="compose"),
    path("result/<int:pk>/", views.ResultView.as_view(), name="result"),
    path("history/", views.HistoryView.as_view(), name="history"),
    path("download/<int:pk>/", views.DownloadView.as_view(), name="download"),
]


