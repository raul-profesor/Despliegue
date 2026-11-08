"""Consulta la altitud de los recintos mediante la API de Open-Meteo.

La API de elevacion de Open-Meteo (https://open-meteo.com/en/docs/elevation-api)
devuelve la altitud del terreno a partir de las coordenadas, usando el modelo
digital de elevacion Copernicus GLO-90.

Este modulo es robusto a proposito: si la API no esta disponible (servidor sin
salida a Internet, por ejemplo), la aplicacion sigue funcionando y simplemente
muestra la altitud estimada que viene en el fichero de datos.
"""

from __future__ import annotations

import logging
import urllib.error
import urllib.parse
import urllib.request

log = logging.getLogger(__name__)

API_URL = "https://api.open-meteo.com/v1/elevation"
TIMEOUT = 5  # segundos


def consultar_altitud(lat: float, lon: float) -> float | None:
    """Devuelve la altitud en metros, o None si no se pudo consultar."""
    params = urllib.parse.urlencode({"latitude": lat, "longitude": lon})
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as respuesta:
            import json

            datos = json.loads(respuesta.read().decode("utf-8"))
            valores = datos.get("elevation") or []
            if valores:
                return float(valores[0])
    except (urllib.error.URLError, OSError, ValueError) as exc:
        log.warning("No se pudo consultar la altitud de (%s, %s): %s", lat, lon, exc)

    return None
