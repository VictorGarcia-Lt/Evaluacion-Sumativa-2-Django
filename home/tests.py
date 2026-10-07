"""Pruebas de la aplicación ``home``.

Cubren los criterios de la Evaluación Sumativa 2: estructura de archivos,
datos del catálogo, enrutamiento con namespace y plantillas heredadas.
"""

from pathlib import Path

from django.http import Http404
from django.test import SimpleTestCase
from django.urls import reverse

from home import views

BASE_DIR = Path(__file__).resolve().parent.parent
CLAVES_PELICULA = {"nombre", "edad", "descripcion", "imagen"}


class EstructuraDeArchivosTests(SimpleTestCase):
    """Verifica que existan todos los archivos y carpetas clave."""

    def test_template_base_existe_y_no_esta_vacio(self):
        ruta = BASE_DIR / "templates" / "base.html"
        self.assertTrue(ruta.exists(), "Falta templates/base.html")
        self.assertGreater(ruta.stat().st_size, 0, "templates/base.html está vacío")

    def test_plantillas_de_la_app_existen(self):
        for nombre in ("inicio.html", "genero.html"):
            ruta = BASE_DIR / "home" / "templates" / "home" / nombre
            self.assertTrue(ruta.exists(), f"Falta home/templates/home/{nombre}")

    def test_carpetas_static_existen(self):
        for carpeta in ("css", "js", "images"):
            ruta = BASE_DIR / "static" / carpeta
            self.assertTrue(ruta.is_dir(), f"Falta static/{carpeta}/")

    def test_archivos_static_basicos_existen(self):
        for ruta in ("css/style.css", "js/main.js"):
            archivo = BASE_DIR / "static" / ruta
            self.assertTrue(archivo.exists(), f"Falta static/{ruta}")
            self.assertGreater(archivo.stat().st_size, 0, f"static/{ruta} está vacío")

    def test_imagenes_de_peliculas_existen(self):
        for genero in views.GENEROS:
            for pelicula in genero["peliculas"]:
                ruta = BASE_DIR / "static" / pelicula["imagen"]
                self.assertTrue(
                    ruta.exists(),
                    f"No existe la imagen de '{pelicula['nombre']}': static/{pelicula['imagen']}",
                )

    def test_gitignore_excluye_lo_requerido(self):
        contenido = (BASE_DIR / ".gitignore").read_text(encoding="utf-8")
        for exclude in (".venv/", "*.sqlite3", "__pycache__/"):
            self.assertIn(exclude, contenido, f".gitignore no excluye {exclude}")

    def test_documentacion_existe(self):
        for nombre in ("README.md", "requirements.txt"):
            self.assertTrue((BASE_DIR / nombre).exists(), f"Falta {nombre}")


class CatalogoTests(SimpleTestCase):
    """Los datos del catálogo cumplen los requisitos de la evaluación."""

    def test_existen_dos_generos_con_descripcion(self):
        self.assertEqual(len(views.GENEROS), 2)
        for genero in views.GENEROS:
            self.assertTrue(genero.get("descripcion"), "Género sin descripción")
            self.assertTrue(genero.get("nombre"), "Género sin nombre")
            self.assertTrue(genero.get("slug"), "Género sin slug")

    def test_cada_genero_tiene_al_dos_peliculas_completas(self):
        for genero in views.GENEROS:
            with self.subTest(genero=genero["slug"]):
                self.assertGreaterEqual(
                    len(genero["peliculas"]), 2,
                    f"'{genero['nombre']}' tiene menos de 2 películas",
                )
                for pelicula in genero["peliculas"]:
                    faltantes = CLAVES_PELICULA - set(pelicula)
                    self.assertFalse(
                        faltantes,
                        f"'{pelicula.get('nombre', '???')}' le falta: {faltantes}",
                    )
                    self.assertIsInstance(pelicula["edad"], int)

    def test_helper_obtener_genero(self):
        self.assertEqual(views.obtener_genero("accion")["nombre"], "Acción")
        with self.assertRaises(Http404):
            views.obtener_genero("no-existe")


class EnrutamientoTests(SimpleTestCase):
    """Namespace de la app y ruta raíz."""

    def test_namespace_de_la_app(self):
        from home.urls import app_name

        self.assertEqual(app_name, "home")

    def test_ruta_raiz_carga_el_inicio(self):
        self.assertEqual(reverse("home:inicio"), "/")

    def test_url_de_accion(self):
        self.assertEqual(reverse("home:genero_accion"), "/accion/")

    def test_url_de_drama(self):
        self.assertEqual(reverse("home:genero_drama"), "/drama/")

    def test_url_espaciada_resuelve(self):
        self.assertEqual(reverse("home:inicio"), "/")


class VistasTests(SimpleTestCase):
    """Respuestas de las vistas y contexto dinámico."""

    def test_inicio_responde_200_con_los_datos(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("home/inicio.html", [t.name for t in respuesta.templates])
        self.assertEqual(len(respuesta.context["generos"]), 2)
        self.assertEqual(respuesta.context["total_generos"], 2)
        self.assertEqual(
            respuesta.context["total_peliculas"],
            sum(len(g["peliculas"]) for g in views.GENEROS),
        )

    def test_vistas_de_generos_entregan_peliculas_en_contexto(self):
        rutas = {"accion": "/accion/", "drama": "/drama/"}
        for slug, ruta in rutas.items():
            with self.subTest(slug=slug):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn("home/genero.html", [t.name for t in respuesta.templates])
                self.assertEqual(respuesta.context["genero"]["slug"], slug)
                self.assertEqual(
                    len(respuesta.context["peliculas"]),
                    len(views.obtener_genero(slug)["peliculas"]),
                )

    def test_vista_genero_inexistente_responde_404(self):
        respuesta = self.client.get("/genero/xyz/")
        self.assertEqual(respuesta.status_code, 404)


class PlantillasTests(SimpleTestCase):
    """Herencia, bucles, condicionales y uso de {% static %}."""

    def _leer(self, *partes):
        return (BASE_DIR.joinpath(*partes)).read_text(encoding="utf-8")

    def test_plantillas_heredan_de_base(self):
        for nombre in ("inicio.html", "genero.html"):
            contenido = self._leer("home", "templates", "home", nombre)
            self.assertIn('{% extends "base.html" %}', contenido)

    def test_base_incluye_bootstrap_5_por_cdn(self):
        base = self._leer("templates", "base.html")
        self.assertIn("cdn.jsdelivr.net/npm/bootstrap@5", base)
        self.assertIn("{% load static %}", base)

    def test_uso_de_bucles_y_condicionales(self):
        for nombre in ("inicio.html", "genero.html"):
            contenido = self._leer("home", "templates", "home", nombre)
            self.assertIn("{% for ", contenido, f"{nombre} sin bucles for")
            self.assertIn("{% if ", contenido, f"{nombre} sin condicionales if")
            self.assertIn("{% static ", contenido, f"{nombre} sin etiqueta static")

    def test_badges_de_edad_condicionales(self):
        contenido = self._leer("home", "templates", "home", "genero.html")
        self.assertIn("pelicula.edad", contenido)
        self.assertIn("edad-badge", contenido)

    def test_imagenes_enlazadas_con_static(self):
        contenido = self._leer("home", "templates", "home", "inicio.html")
        self.assertIn("{% static pelicula.imagen %}", contenido)
