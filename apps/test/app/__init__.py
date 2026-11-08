"""Records mundiales de medio fondo y fondo de atletismo.

Aplicacion Flask que muestra los records mundiales vigentes de medio fondo y
fondo, indicando donde se consequieron mediante un mapa interactivo.

Estructura:

    /            -> Pagina principal con el mapa y la tabla de records
    /api/records -> Los records en formato JSON
    /api/recintos -> Los recintos con sus coordenadas
    /api/altitud  -> Consulta la altitud de un recinto
    /health       -> Sonda de salud (util para el despliegue)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import date

from flask import Flask, jsonify, render_template, request

from . import datos
from .elevacion import consultar_altitud

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

app = Flask(__name__)

# La clave secreta se lee del entorno. En produccion la inyecta systemd
# mediante EnvironmentFile; en desarrollo se usa un valor por defecto.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "clave-de-desarrollo-no-usar-en-produccion")


@app.route("/")
def index():
    """Pagina principal: mapa + tabla de records filtrable."""
    records = datos.obtener_records()

    categoria = request.args.get("categoria") or None
    sexo = request.args.get("sexo") or None
    modalidad = request.args.get("modalidad") or None
    texto = request.args.get("q") or None

    filtrados = datos.filtrar(
        records, categoria=categoria, sexo=sexo, modalidad=modalidad, texto=texto
    )

    # Enriquecemos con los recintos unicos de los records filtrados.
    # Cada recinto lleva sus pruebas para poder mostrarlas en el popup.
    recintos: dict[str, dict] = {}
    for record in filtrados:
        clave = record["recinto"]
        if clave not in recintos:
            recintos[clave] = {
                "id": clave,
                "nombre": record["recinto_nombre"],
                "ciudad": record["ciudad"],
                "pais": record["pais_recinto"],
                "lat": record["lat"],
                "lon": record["lon"],
                "altitud_estimada": record["altitud_estimada"],
                "modalidades": [],
                "pruebas": [],
            }
        recinto = recintos[clave]
        if record["modalidad"] not in recinto["modalidades"]:
            recinto["modalidades"].append(record["modalidad"])
        recinto["pruebas"].append(
            {
                "prueba": record["prueba"],
                "marca": record["marca"],
                "atleta": record["atleta"],
                "sexo": record["sexo"],
            }
        )

    lista_recintos = list(recintos.values())

    return render_template(
        "index.html",
        records=filtrados,
        recintos=lista_recintos,
        recintos_json=json.dumps(lista_recintos, ensure_ascii=False),
        total=len(records),
        categorias=datos.categorias(),
        sexos=datos.sexos(),
        filtros={
            "categoria": categoria or "",
            "sexo": sexo or "",
            "modalidad": modalidad or "",
            "q": texto or "",
        },
        hoy=date.today().isoformat(),
    )


@app.route("/api/records")
def api_records():
    """Devuelve los records en formato JSON, respetando los filtros."""
    records = datos.obtener_records()
    filtrados = datos.filtrar(
        records,
        categoria=request.args.get("categoria") or None,
        sexo=request.args.get("sexo") or None,
        modalidad=request.args.get("modalidad") or None,
        texto=request.args.get("q") or None,
    )
    return jsonify({"total": len(filtrados), "records": filtrados})


@app.route("/api/recintos")
def api_recintos():
    """Devuelve los recintos donde se han marcado records."""
    return jsonify({"recintos": datos.obtener_recintos_usados()})


@app.route("/api/altitud")
def api_altitud():
    """Consulta la altitud de un recinto mediante la API de Open-Meteo."""
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Se requieren los parametros 'lat' y 'lon'"}), 400

    altitud = consultar_altitud(lat, lon)
    if altitud is None:
        return jsonify({"error": "No se pudo consultar la altitud"}), 503

    return jsonify({"lat": lat, "lon": lon, "altitud": altitud})


@app.route("/health")
def health():
    """Sonda de salud. Devuelve 200 si la aplicacion puede servir."""
    try:
        total = len(datos.obtener_records())
    except datos.DatosNoDisponibles as exc:
        return jsonify({"estado": "error", "detalle": str(exc)}), 503

    return jsonify({"estado": "ok", "records": total})
