"""Vistas de la aplicación ``home``.

Este módulo concentra el catálogo estático de películas del proyecto:

* 2 géneros de películas, cada uno con su descripción.
* Mínimo 2 películas por género, con ``nombre``, ``edad``, ``descripcion``
  e ``imagen``.

Los datos se entregan **dinámicamente** a las plantillas mediante el
``context`` de cada vista (nada está escrito a mano dentro de los HTML).
"""

from django.http import Http404
from django.shortcuts import render

GENEROS = [
    {
        "slug": "ciencia-ficcion",
        "nombre": "Ciencia Ficción",
        "descripcion": (
            "Futuros posibles, viajes interestelares y tecnología que pone a "
            "prueba todo lo que creíamos saber sobre nosotros mismos."
        ),
        "imagen": "images/generos/ciencia-ficcion.svg",
        "peliculas": [
            {
                "nombre": "Órbita 9",
                "edad": 12,
                "anio": 2024,
                "descripcion": (
                    "La tripulación de una estación de reciclaje orbital "
                    "despierta tras 40 años de hibernación para descubrir "
                    "que la Tierra dejó de responder a sus señales."
                ),
                "imagen": "images/peliculas/orbita-9.svg",
            },
            {
                "nombre": "Eco de Marte",
                "edad": 14,
                "anio": 2025,
                "descripcion": (
                    "Una geóloga detecta una señal rítmica bajo el hielo "
                    "marciano y debe decidir si avisar a la Tierra o "
                    "continuar sola con la excavación."
                ),
                "imagen": "images/peliculas/eco-de-marte.svg",
            },
            {
                "nombre": "Neón Profundo",
                "edad": 16,
                "anio": 2023,
                "descripcion": (
                    "En una ciudad sumergida, un hacker reconstruye la "
                    "memoria de un androide para probar su inocencia ante "
                    "un crimen que él no recuerda cometer."
                ),
                "imagen": "images/peliculas/neon-profundo.svg",
            },
            {
                "nombre": "El Último Circuit",
                "edad": 18,
                "anio": 2026,
                "descripcion": (
                    "Cuando la red que gobierna al mundo se apaga, un "
                    "ingeniero retirado descubre que apagarla fue apenas "
                    "el primer paso de un plan mucho más grande."
                ),
                "imagen": "images/peliculas/ultimo-circuit.svg",
            },
        ],
    },
    {
        "slug": "comedia",
        "nombre": "Comedia",
        "descripcion": (
            "Situaciones descontroladas, enredos cotidianos y personajes "
            "que siempre terminan empeorando lo que intentan arreglar."
        ),
        "imagen": "images/generos/comedia.svg",
        "peliculas": [
            {
                "nombre": "Mi tío astronauta",
                "edad": 7,
                "anio": 2024,
                "descripcion": (
                    "Un niño convence a su excéntrico tío de simular un "
                    "viaje espacial en el jardín trasero y el engaño se "
                    "le escapa de las manos a todo el barrio."
                ),
                "imagen": "images/peliculas/mi-tio-astronauta.svg",
            },
            {
                "nombre": "Los reemplazos",
                "edad": 12,
                "anio": 2025,
                "descripcion": (
                    "Cinco empleados descubren que su empresa los clonó "
                    "para despedirlos sin pagar indemnización y ahora "
                    "deben competir contra sus propios dobles."
                ),
                "imagen": "images/peliculas/los-reemplazos.svg",
            },
            {
                "nombre": "Cita a ciegas",
                "edad": 14,
                "anio": 2023,
                "descripcion": (
                    "Dos perfiles falsos, creados a espaldas de sus dueños, "
                    "terminan citándose en la vida real sin saber que "
                    "ambos mintieron en absolutamente todo."
                ),
                "imagen": "images/peliculas/cita-a-ciegas.svg",
            },
            {
                "nombre": "Jefe de honor",
                "edad": 18,
                "anio": 2026,
                "descripcion": (
                    "El equipo de una agencia organiza la despedida de su "
                    "jefe jubilado y descubre, demasiado tarde, que el "
                    "homenaje estaba dedicado a otra persona."
                ),
                "imagen": "images/peliculas/jefe-de-honor.svg",
            },
        ],
    },
]

def obtener_generos() -> list:
  
    return GENEROS


def obtener_genero(slug: str) -> dict:
    
    for genero in GENEROS:
        if genero["slug"] == slug:
            return genero
    raise Http404(f"No existe el género solicitado: {slug}")


def inicio(request):
    
    generos = obtener_generos()
    context = {
        "titulo": "Inicio",
        "generos": generos,
        "total_generos": len(generos),
        "total_peliculas": sum(len(g["peliculas"]) for g in generos),
    }
    return render(request, "home/inicio.html", context)


def genero(request, slug: str):
    
    genero_actual = obtener_genero(slug)
    context = {
        "titulo": genero_actual["nombre"],
        "generos": obtener_generos(),  
        "genero": genero_actual,
        "peliculas": genero_actual["peliculas"],
        "total_peliculas": len(genero_actual["peliculas"]),
    }
    return render(request, "home/genero.html", context)
