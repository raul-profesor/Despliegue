# Records mundiales de medio fondo y fondo

Aplicación web Flask que muestra los **records mundiales vigentes de medio fondo y fondo** de atletismo, indicando **dónde y cuándo se consequieron**, mediante un mapa interactivo.

Es la aplicación real que se despliega en la [Práctica 3.5 — Despliegue de una aplicación Flask](https://raul-profesor.github.io/Despliegue/Tema3/P3.5.nueva/).

## Características

- **Mapa interactivo** (Leaflet + OpenStreetMap) con un marcador por recinto, dimensionado según su altitud.
- **Tabla filtrable** por categoría, sexo, modalidad y texto libre (la búsqueda ignora acentos y mayúsculas).
- **API JSON** para consumir los datos desde otras herramientas.
- **Altitud del terreno** consultada en tiempo de ejecución a la API de elevación de Open-Meteo (Copernicus GLO-90).
- **Degradación elegante**: si la API de Open-Meteo no responde, la aplicación sigue funcionando con la altitud estimada del JSON.
- **Sonda de salud** en `/health`, pensada para usarla desde `systemd` o un monitor de despliegue.

## Estructura

```text
aplicacion/
├── app/
│   ├── __init__.py          # Rutas Flask
│   ├── datos.py             # Carga y filtrado de los datos
│   ├── elevacion.py         # Consulta a la API de Open-Meteo
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/estilo.css
│       └── js/mapa.js
├── data/
│   └── records.json         # Records y recintos
├── requirements.txt
└── wsgi.py                  # Punto de entrada para Gunicorn
```

## Puesta en marcha

Con [`uv`](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
uv run flask --app wsgi run --host 0.0.0.0 --port 5000
```

O con las herramientas estándar:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app wsgi run --host 0.0.0.0 --port 5000
```

!!! warning "`uv pip` busca hacia arriba"
    `uv pip install` busca un `pyproject.toml` en el directorio actual y en sus padres, y si encuentra uno instala en el entorno virtual de ese proyecto. Si tu proyecto está dentro de otro que tiene `pyproject.toml`, indica el entorno explícitamente:

    ```bash
    VIRTUAL_ENV="$PWD/.venv" uv pip install -r requirements.txt
    ```

## Despliegue

```bash
.venv/bin/gunicorn --workers 4 --bind unix:/run/flask/atletismo.sock wsgi:app
```

## API

| Ruta | Descripción |
|---|---|
| `GET /` | Página principal con mapa y tabla |
| `GET /api/records` | Records en JSON (admite `categoria`, `sexo`, `modalidad`, `q`) |
| `GET /api/recintos` | Recintos con sus coordenadas y pruebas |
| `GET /api/altitud?lat=&lon=` | Altitud del terreno según Open-Meteo |
| `GET /health` | Sonda de salud |

## Fuentes de datos

- **Records**: [World Athletics](https://worldathletics.org/records) (World Records, por disciplina). Datos verificados a **8 de noviembre de 2026**.
- **Altitud**: [Open-Meteo Elevation API](https://open-meteo.com/en/docs/elevation-api), modelo digital de elevación Copernicus GLO-90.
- **Mapa base**: [OpenStreetMap](https://www.openstreetmap.org/copyright) © colaboradores de OSM.

!!! warning "Los records cambian"
    Un record mundial puede ser superado en cualquier momento. Los datos de `data/records.json` están fechados en el momento de elaborarlos y conviene revisarlos antes de cada curso.

    La marca de **media maratón femenina** (56:51, Yomif Kejelcha, Buenos Aires, 23-08-2026) estaba **pendiente de ratificación** en la fecha de verificación. Se marca como tal en el campo `notas` del registro.
