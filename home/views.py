from django.http import Http404
from django.shortcuts import render

# Catálogo de películas organizado por género.
GENEROS = [
    {
        "slug": "accion",
        "vista": "home:genero_accion",
        "nombre": "Acción",
        "descripcion": (
            "Persecuciones, misiones de alto riesgo y protagonistas que "
            "lo arriesgan todo para salvar el día."
        ),
        "imagen": "images/generos/accion.svg",
        "peliculas": [
            {
                "nombre": "Rescate Extremo",
                "edad": 12,
                "anio": 2024,
                "descripcion": (
                    "Un equipo de rescate de montaña enfrenta una tormenta "
                    "para salvar a un grupo de alpinistas atrapados en la cima."
                ),
                "imagen": "images/peliculas/rescate-extremo.svg",
            },
            {
                "nombre": "Velocidad Máxima",
                "edad": 14,
                "anio": 2025,
                "descripcion": (
                    "Un conductor de ambulancias debe cruzar la ciudad en "
                    "tiempo récord mientras una banda de mercenarios lo persigue."
                ),
                "imagen": "images/peliculas/velocidad-maxima.svg",
            },
            {
                "nombre": "Operación Cóndor",
                "edad": 16,
                "anio": 2023,
                "descripcion": (
                    "Una agente encubierta se infiltra en una red internacional "
                    "de contrabando para desmantelarla desde adentro."
                ),
                "imagen": "images/peliculas/operacion-condor.svg",
            },
            {
                "nombre": "El Último Comando",
                "edad": 18,
                "anio": 2026,
                "descripcion": (
                    "Un comando de élite retirado vuelve a la acción cuando "
                    "su base es atacada en plena noche."
                ),
                "imagen": "images/peliculas/ultimo-comando.svg",
            },
        ],
    },
    {
        "slug": "drama",
        "vista": "home:genero_drama",
        "nombre": "Drama",
        "descripcion": (
            "Historias humanas intensas, decisiones difíciles y personajes "
            "que buscan un segundo comienzo."
        ),
        "imagen": "images/generos/drama.svg",
        "peliculas": [
            {
                "nombre": "Cartas al Abuelo",
                "edad": 7,
                "anio": 2024,
                "descripcion": (
                    "Un niño encuentra las cartas que su abuelo nunca envió "
                    "y recorre su pueblo para entregarlas una por una."
                ),
                "imagen": "images/peliculas/cartas-al-abuelo.svg",
            },
            {
                "nombre": "El Camino de Regreso",
                "edad": 12,
                "anio": 2025,
                "descripcion": (
                    "Un músico que perdió la inspiración vuelve a su pueblo "
                    "natal para redescubrir por qué empezó a tocar."
                ),
                "imagen": "images/peliculas/camino-de-regreso.svg",
            },
            {
                "nombre": "Entre Dos Mundos",
                "edad": 14,
                "anio": 2023,
                "descripcion": (
                    "Una estudiante de intercambio se adapta a un nuevo país "
                    "mientras su familia enfrenta una crisis a la distancia."
                ),
                "imagen": "images/peliculas/entre-dos-mundos.svg",
            },
            {
                "nombre": "La Deuda",
                "edad": 18,
                "anio": 2026,
                "descripcion": (
                    "Un abogado descubre que el caso que lo hizo famoso "
                    "escondía una verdad que cambiará su vida para siempre."
                ),
                "imagen": "images/peliculas/la-deuda.svg",
            },
        ],
    },
]


def obtener_generos():
    return GENEROS


def obtener_genero(slug):
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
        "total_peliculas": sum(len(genero["peliculas"]) for genero in generos),
    }
    return render(request, "home/inicio.html", context)


def _contexto_genero(genero_actual):
    return {
        "titulo": genero_actual["nombre"],
        "generos": obtener_generos(),
        "genero": genero_actual,
        "peliculas": genero_actual["peliculas"],
        "total_peliculas": len(genero_actual["peliculas"]),
    }


def genero_accion(request):
    return render(request, "home/genero.html", _contexto_genero(obtener_genero("accion")))


def genero_drama(request):
    return render(request, "home/genero.html", _contexto_genero(obtener_genero("drama")))