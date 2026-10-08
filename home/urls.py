from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("accion/", views.genero_accion, name="genero_accion"),
    path("drama/", views.genero_drama, name="genero_drama"),
]
