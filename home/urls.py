from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    # Ruta principal accesibles desde /
    path("", views.inicio, name="inicio"),
    
    # Rutas fijas para cada uno de los dos géneros
    path("accion/", views.genero_accion, name="genero_accion"),
    path("drama/", views.genero_drama, name="genero_drama"),
]