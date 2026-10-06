"""URLs de la aplicación ``home``.

``app_name`` define el *namespace* de la app, por lo que en cualquier
plantilla deben usarse los nombres espaciados: ``{% url 'home:inicio' %}``.
"""

from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("genero/<slug:slug>/", views.genero, name="genero"),
]
