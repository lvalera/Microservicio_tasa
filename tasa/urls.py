# tasa/urls.py

from django.urls import path
from .views import TasaVigenteView

urlpatterns = [
    # Cuando alguien visite '.../vigente/', se llamará a TasaVigenteView
    path("vigente/", TasaVigenteView.as_view(), name="tasa-vigente"),
]
