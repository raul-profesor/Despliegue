"""Carga y consulta de los datos de recordselters de atletismo.

Este modulo encapsula todo el acceso a los datos: el resto de la aplicacion
no sabe nada de donde vienen los records, solo pide records y los recibe.
"""

from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RECORDS_FILE = DATA_DIR / "records.json"

# Etiquetas legibles para los codigos de pais
PAISES = {
    "AUS": "Australia",
    "AUT": "Austria",
    "BEL": "Belgica",
    "BRA": "Brasil",
    "CHN": "China",
    "ETH": "Etiopia",
    "FRA": "Francia",
    "GBR": "Reino Unido",
    "GER": "Alemania",
    "HUN": "Hungria",
    "ITA": "Italia",
    "KEN": "Kenia",
    "MAR": "Marruecos",
    "MCO": "Monaco",
    "MEX": "Mexico",
    "MON": "Monaco",
    "NED": "Paises Bajos",
    "NOR": "Noruega",
    "PER": "Peru",
    "SLO": "Eslovenia",
    "SUI": "Suiza",
    "UGA": "Uganda",
    "USA": "Estados Unidos",
}


class DatosNoDisponibles(Exception):
    """Se lanza cuando el fichero de datos no existe o esta corrupto."""


@lru_cache(maxsize=1)
def _cargar_datos() -> dict:
    """Lee el JSON de datos y lo cachea en memoria."""
    try:
        with RECORDS_FILE.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as exc:
        raise DatosNoDisponibles(
            f"No se encuentra el fichero de datos: {RECORDS_FILE}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise DatosNoDisponibles(
            f"El fichero de datos no contiene JSON valido: {exc}"
        ) from exc


def obtener_records() -> list[dict]:
    """Devuelve todos los records, enriquecidos con los datos de su recinto."""
    datos = _cargar_datos()
    recintos = datos.get("recintos", {})

    enriquecidos = []
    for record in datos.get("records", []):
        recinto = recintos.get(record["recinto"], {})
        item = dict(record)
        item["recinto_nombre"] = recinto.get("nombre", "Desconocido")
        item["ciudad"] = recinto.get("ciudad", "")
        item["pais_recinto"] = recinto.get("pais", "")
        item["lat"] = recinto.get("lat")
        item["lon"] = recinto.get("lon")
        item["altitud_estimada"] = recinto.get("altitud_estimada")
        item["pais_nombre"] = PAISES.get(record.get("pais_atleta", ""), "")
        enriquecidos.append(item)

    return enriquecidos


def obtener_recintos_usados() -> list[dict]:
    """Devuelve la lista de recintos donde se ha marcado algun record."""
    vistos: dict[str, dict] = {}
    for record in obtener_records():
        clave = record["recinto"]
        if clave in vistos:
            vistos[clave]["records"].append(record)
        else:
            vistos[clave] = {
                "id": clave,
                "nombre": record["recinto_nombre"],
                "ciudad": record["ciudad"],
                "pais": record["pais_recinto"],
                "lat": record["lat"],
                "lon": record["lon"],
                "altitud_estimada": record["altitud_estimada"],
                "records": [record],
            }
    return list(vistos.values())


def categorias() -> list[str]:
    """Categorias de prueba disponibles (medio fondo y fondo)."""
    return ["Medio fondo", "Fondo"]


def sexos() -> list[str]:
    return ["Hombres", "Mujeres"]


def modalidad_por_defecto(categoria: str) -> str:
    """Modalidad mas habitual dentro de una categoria."""
    return "pista"


def _normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, para que la busqueda sea tolerante."""
    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return sin_acentos.lower()


# Un solo diccionario para no recalcular la normalizacion en cada busqueda
_BUSQUEDA = {
    "atleta": ["atleta"],
    "prueba": ["prueba"],
    "recinto": ["recinto_nombre"],
    "ciudad": ["ciudad"],
    "pais_atleta": ["pais_atleta", "pais_nombre"],
    "pais_recinto": ["pais_recinto"],
}


def filtrar(
    records: list[dict],
    categoria: str | None = None,
    sexo: str | None = None,
    modalidad: str | None = None,
    texto: str | None = None,
) -> list[dict]:
    """Filtra la lista de records por los criterios indicados."""
    resultado = records

    if categoria:
        resultado = [r for r in resultado if r["categoria"] == categoria]

    if sexo:
        resultado = [r for r in resultado if r["sexo"] == sexo]

    if modalidad:
        resultado = [r for r in resultado if r["modalidad"] == modalidad]

    if texto:
        aguja = _normalizar(texto)
        if aguja:
            def coincide(record: dict) -> bool:
                for campos in _BUSQUEDA.values():
                    for campo in campos:
                        if aguja in _normalizar(str(record.get(campo, ""))):
                            return True
                return False

            resultado = [r for r in resultado if coincide(r)]

    return resultado
