"""Punto de entrada WSGI para Gunicorn.

Gunicorn localizara la instancia de Flask con la sintaxis `wsgi:app`.
"""

from app import app

__all__ = ["app"]
