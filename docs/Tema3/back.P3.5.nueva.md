---
title: Práctica 3.4 - Despliegue de una aplicación Flask
icon: material/language-python
---

# Práctica 3.4: Despliegue de una aplicación Flask

## 1. Objetivos

Al finalizar la práctica, seremos capaces de:

- Comprender la arquitectura de tres capas de una aplicación web Python: servidor web (Nginx), servidor de aplicaciones WSGI (Gunicorn) y framework de aplicación (Flask).
- Explicar qué es un framework web, qué es Flask como *microframework* y en qué consiste el patrón MVC.
- Explicar qué es WSGI, para qué sirve y por qué existe un estándar de comunicación entre servidores web y aplicaciones Python.
- Gestionar las dependencias de un proyecto Python con `uv`, sustituyendo a las soluciones clásicas basadas en `pipenv`.
- Crear entornos virtuales reproducibles con `uv venv` e instalar dependencias con `uv pip install -r requirements.txt`.
- Desplegar una aplicación Flask mínima y, posteriormente, una aplicación real completa desde un repositorio de GitHub.
- Desplegar **dos aplicaciones simultáneas** en el mismo servidor, cada una con su propio servicio, socket y virtual host.
- Ejecutar Gunicorn en modo manual, tanto escuchando en un puerto TCP como en un socket Unix.
- Crear una unidad de servicio de `systemd` robusta, con reinicio automático, recarga sin downtime y directivas de hardening.
- Configurar Nginx como proxy inverso hacia Gunicorn utilizando un socket Unix.
- Diagnosticar los errores más habituales del proceso de despliegue.
- Comprobar que una aplicación que **depende de un servicio externo** sigue funcionando cuando ese servicio no responde.

---

## 2. Requisitos previos

- Un servidor (físico, virtual o en la nube) con Debian 12 (Bookworm) o Ubuntu 22.04/24.04 LTS y acceso por SSH.
- Usuario con privilegios de `sudo` en dicho servidor.
- Conexión SSH funcional desde tu máquina local al servidor.
- Acceso a GitHub y al repositorio [`raul-profesor/atletismo-records`](https://github.com/raul-profesor/atletismo-records), que es la aplicación que se despliega en la segunda parte.

---

## 3. Conocimientos previos

Antes de comenzar conviene tener claros algunos conceptos, porque aparecen a lo largo de toda la práctica.

### 3.1. ¿Qué es un framework web?

En el desarrollo moderno de aplicaciones web se utilizan distintos **frameworks**, que son herramientas que nos dan un esquema de trabajo y una serie de utilidades y funciones que nos facilita y nos abstrae de la construcción de páginas web dinámicas.

En general, los frameworks están asociados a lenguajes de programación (Ruby on Rails para Ruby, Symfony para PHP, Spring Boot para Java). En el mundo de Python el más conocido es Django, pero **Flask** es una opción que quizá no tenga una curva de aprendizaje tan elevada y, aun así, nos posibilita la creación de aplicaciones web igual de complejas que las que se pueden crear en Django.

### 3.2. Flask

Flask es un «micro» framework escrito en Python y concebido para facilitar el desarrollo de aplicaciones web bajo el patrón MVC.

La palabra «micro» no designa a que sea un proyecto pequeño ni a que nos permita hacer páginas web pequeñas. Al instalar Flask tenemos las herramientas necesarias para crear una aplicación web funcional, pero si se necesita en algún momento una nueva funcionalidad hay un conjunto muy grande de extensiones (plugins) que se pueden instalar y que dotan a la aplicación de nueva funcionalidad.

![](../img/flask.png){: style="height:300px;width:550px"}

De principio en la instalación no se tienen todas las funcionalidades que se pueden necesitar, pero de una manera muy sencilla se pueden extender el proyecto con nuevas funcionalidades por medio de plugins.

### 3.3. El patrón MVC

El patrón MVC es una forma de trabajar que permite diferenciar y separar lo que es:

| Capa | Responsabilidad | En Flask |
|---|---|---|
| **Modelo** | Los datos de la aplicación, normalmente almacenados en una base de datos | Objetos Python, ORM (SQLAlchemy), ficheros |
| **Vista** | La presentación en HTML | Plantillas Jinja2 en `templates/` |
| **Controlador** | La gestión de las peticiones: qué ruta llama a qué lógica | Las funciones Python decoradas con `@app.route()` |

### 3.4. Gunicorn

Cuando se implementa una aplicación web basada en Python, normalmente se tienen estas tres piezas:

1. **Servidor web** (Nginx, Apache): procesa y distribuye las solicitudes de los navegadores y otros clientes.
2. **Servidor de aplicaciones WSGI** (Gunicorn, uWSGI, mod_wsgi, Waitress): intermedia entre el servidor web y la aplicación.
3. **Aplicación web** (Django, Flask, Pyramid, FastAPI).

**WSGI** (Web Server Gateway Interface) proporciona un conjunto de reglas para estandarizar el comportamiento y la comunicación entre servidores web y aplicaciones web. Mediante el uso de servidores y aplicaciones compatibles con WSGI, los desarrolladores pueden concentrar su tiempo y energía en el desarrollo de aplicaciones web en lugar de administrar la comunicación entre la aplicación y el servidor web.

![](../img/gunicorn.png){: style="height:300px;width:550px"}

Gunicorn, que es la abreviatura de *Green Unicorn*, es un servidor de aplicaciones WSGI que se encuentra entre el servidor web y su aplicación web, gestionando la comunicación entre los dos. Acepta solicitudes del servidor y las traduce (a través de WSGI) en algo que la aplicación web puede entender antes de pasarla a la aplicación real. Envía respuestas desde la aplicación web al servidor. También se encarga de ejecutar varias instancias de la aplicación web, reiniciándolas según sea necesario y distribuyendo solicitudes a instancias saludables.

!!! info "El modelo de Gunicorn: prefork"
    Gunicorn sigue un modelo **prefork**: un proceso *master* lanza varios procesos *workers*, cada uno con su propia copia de la aplicación Python. El master se encarga de aceptar conexiones y distribuirlas entre los workers; si un worker muere, el master lo reemplaza automáticamente. Esto es exactamente lo que hace un servidor como Apache con `mod_php` o PHP-FPM, y es lo que lo diferencia del modelo *threaded* de Node.js.

### 3.5. `pip`: el gestor de paquetes de Python

`pip` es el comando para instalar paquetes de Python integrados en las fuentes desde la versión 3.4.

Este comando automatiza la conexión al sitio `https://pypi.org/`, la descarga, la instalación e incluso la compilación del módulo solicitado. Además, se ocupa de las dependencias de cada paquete.

### 3.6. Entornos virtuales de Python

Un entorno virtual es una forma de tener múltiples instancias paralelas del intérprete de Python, cada una con diferentes conjuntos de paquetes y diferentes configuraciones. Cada entorno virtual contiene una copia independiente del intérprete de Python, incluyendo copias de sus utilidades de soporte.

Los paquetes instalados en cada entorno virtual sólo se ven en ese entorno virtual y en ningún otro. Incluso los paquetes grandes y complejos con binarios dependientes de la plataforma pueden quedar aislados entre sí.

De esta forma tendremos entornos independientes entre sí, parecido a lo que ocurre con los directorios de los proyectos de Node.js. Los entornos virtuales de Python nos permiten instalar un paquete en una ubicación aislada en lugar de instalarlo de manera global.

---

## 4. `uv`: el gestor de dependencias moderno de Python

En el enunciado original de esta práctica se utilizaba **Pipenv**. Hoy en día la opción estándar en la industria es **`uv`**, escrito en Rust por el equipo de Astral (los mismos creadores de `ruff`). Esta sección explica qué es y por qué lo vamos a utilizar.

### 4.1. ¿Qué es `uv`?

`uv` es un **gestor de proyectos y paquetes Python** que unifica en una sola herramienta 
varias piezas que antes estaban separadas:

| Función | Herramienta clásica | Con `uv` |
|---|---|---|
| Descargar e instalar paquetes | `pip` | `uv pip install` |
| Resolver dependencias | `pip` (con `pip-tools`) | `uv pip compile` / `uv pip sync` |
| Crear entornos virtuales | `python -m venv` / `virtualenv` | `uv venv` |
| Fijar versiones exactas | `pip freeze` | `uv pip freeze` / `uv.lock` |
| Instalar Python si no lo tienes | `pyenv` | `uv python install` |
| Ejecutar dentro del entorno | `source .venv/bin/activate` | `uv run` |

En resumen: **`uv` es un reemplazo directo de `pip` + `venv` + `pipenv`**, y además es entre 10 y 100 veces más rápido porque está escrito en Rust y resuelve dependencias de forma asíncrona y en paralelo.

### 4.2. Instalación

`uv` se distribuye como un binario autónomo, de forma similar a como se instalaba `pipenv`. La instalación oficial es un script que descarga el binario appropriate para tu sistema:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Recargamos la shell para que `~/.local/bin` esté en el `PATH`:

```bash
source ~/.bashrc
uv --version
```

!!! tip "También disponible en los repositorios de Debian/Ubuntu"
    En Debian 13 (Trixie) y Ubuntu 25.04 o superiores, `uv` está disponible como paquete nativo: `sudo apt install uv`. En versiones anteriores, el script de instalación es la vía recomendada porque instala una versión mucho más reciente.

!!! note "`uv` no necesita Python instalado"
    A diferencia de `pipenv`, `uv` es un binario autónomo: **no depende de Python para ejecutarse**. Sí necesita un intérprete de Python disponible para poder crear entornos virtuales e instalar código con extensiones compiladas, pero puede descargarse él mismo (`uv python install 3.12`).

### 4.3. Uso básico

```bash
# Crear el entorno virtual (crea el directorio .venv/)
uv venv

# Crear el entorno con una versión concreta de Python
uv venv --python 3.12

# Instalar las dependencias declaradas en requirements.txt
uv pip install -r requirements.txt

# Instalar un paquete suelto
uv pip install gunicorn

# Ver lo que hay instalado
uv pip list

# Congelar las dependencias a versions exactas
uv pip freeze > requirements.txt

# Ejecutar un comando dentro del entorno, sin activarlo
uv run gunicorn --workers 4 wsgi:app
```

!!! info "`uv pip` encuentra el entorno automáticamente"
    No hace falta activar el entorno virtual. `uv pip` busca, en este orden: un entorno activado (`$VIRTUAL_ENV`), un `.venv` en el directorio actual o en el directorio padre más cercano. Si no lo encuentra, te lo dirá y te propondrá crearlo.

### 4.4. Pipenv, `pip` + `venv` o `uv`?

Esta es la pregunta natural que surge al modernizar la práctica. Las tres opciones son válidas, pero con diferencias importantes:

| Característica | `pipenv` | `pip` + `venv` | `uv` |
|---|---|---|---|
| Aislamiento del entorno | Automático (`pipenv shell`) | Manual (`python -m venv`) | Automático (`uv venv`) |
| Fichero de declaración de dependencias | `Pipfile` (+ `Pipfile.lock`) | `requirements.txt` | `requirements.txt`, `pyproject.toml` o `uv.lock` |
| Velocidad | Lenta | Lenta | **Muy rápida** (10–100×) |
| Formato de bloqueo | JSON en `Pipfile.lock` | `pip freeze` a mano | `uv.lock` (TOML, universal) |
| Estado del proyecto | Prácticamente abandoned (última release estable en 2023) | Estándar de facto, siempre disponible | **Estándar de facto actual** |
| Instala Python si falta | No | No | **Sí** (`uv python install`) |
| Disponible en los repos de Debian | `sudo apt install pipenv` | Incluido en Python | `sudo apt install uv` (recientes) |

!!! warning "Por qué `pipenv` dejó de ser la recomendación"
    Pipenv ha quedado obsoleto: su formato `Pipfile` era una idea interesante, pero en la práctica obligaba a mantener **dos** sistemas de declaración de dependencias (`Pipfile` para desarrollo y `requirements.txt` para despliegue), lo que generaba duplicidad y desincronización. Además su resolución de dependencias era muy lenta. La comunidad pythonista se ha ido hacia `pip` + `venv` con `requirements.txt`, y más recientemente hacia `uv`, que resuelve el mismo problema mucho mejor.

!!! tip "Alternativa sin `uv`"
    Si en tu servidor no puedes instalar `uv` (políticas restrictivas, por ejemplo), el equivalente exacto con herramientas estándar es:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

    Todo lo demás de la práctica (ruta del ejecutable, unidad de `systemd`, configuración de Nginx) es **exactamente igual**, porque lo importante es la ruta al binario `gunicorn` dentro del entorno virtual.

---

## 5. Arquitectura que vamos a montar

La aplicación que serviremos es una aplicación Flask clásica, con la arquitectura de tres capas típica:

```mermaid
graph LR
    C[Cliente<br/>navegador] -->|HTTP :80| N[Nginx<br/>proxy inverso]
    N -->|socket Unix| G[Gunicorn<br/>master + 4 workers]
    G -->|WSGI| A[Flask<br/>wsgi:app]
    A --> T[Plantillas Jinja2<br/>y ficheros estáticos]
```

El recorrido de una petición es el siguiente:

1. El navegador del cliente abre una conexión TCP contra el **puerto 80** y envía una petición HTTP.
2. **Nginx** recibe la petición. Como la URI no corresponde a ningún fichero estático, la envía al **proxy inverso**.
3. **Gunicorn** tiene un proceso *master* que acepta la conexión y la reparte entre sus procesos *worker*.
4. El *worker* **traduce la petición HTTP a una llamada WSGI** y se la pasa a la **aplicación Flask**.
5. Flask ejecuta la función de la ruta, renderiza la plantilla Jinja2 y devuelve una respuesta WSGI.
6. La respuesta recorre el camino inverso: Flask → Gunicorn → Nginx → cliente.

!!! note "Por qué el socket Unix y no un puerto TCP"
    Entre Nginx y Gunicorn, que están en **la misma máquina**, no tiene sentido abrir un puerto TCP: el socket Unix es un fichero especial del sistema de ficheros que permite la comunicación local entre procesos. Es más rápido (no pasa por la pila de red), no es alcanzable desde el exterior y hereda directamente los permisos del usuario del servicio. Lo veremos en detalle en el [Paso 9](#paso-9-convertir-gunicorn-en-un-servicio-de-systemd).

!!! info "Gunicorn vs el servidor de desarrollo de Flask"
    El servidor de desarrollo de Flask (`flask run` o `app.run()`) es un servidor de desarrollo: **no es un servidor de producción**. Lo explicaremos con más detalle en el [Paso 7](#paso-7-probar-con-el-servidor-de-desarrollo-de-flask).

---

## 6. Aplicación a desplegar

En esta práctica trabajaremos con **dos** aplicaciones: una mínima, para entender los conceptos sin distracciones, y una real, para ver un despliegue completo.

### 6.1. Aplicación PoC (proof of concept)

La primera aplicación es la más simple posible, a modo de prueba de concepto. Consta de dos ficheros:

- `application.py`: contiene la aplicación Flask propiamente dicha.
- `wsgi.py`: se encarga únicamente de importarla y exponerla como objeto WSGI, que es lo que Gunicorn espera.

El contenido de `application.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Mi aplicacion Flask</h1><p>Desplegada con Nginx + Gunicorn</p>"


if __name__ == "__main__":
    app.run()
```

Y el de `wsgi.py`:

```python
from application import app

# Gunicorn.expecta encontrar un objeto WSGI llamado 'app' en este módulo
__all__ = ["app"]
```

!!! info "¿Por qué un `wsgi.py` aparte?"
    Porque separa la **aplicación** (lo que el desarrollador escribe y despliega) del **punto de entrada** que consume el servidor. Cuando la aplicación crece, el `wsgi.py` es el sitio natural donde configurar cosas como el objeto de contexto, los blueprints o el middleware. Además, Gunicorn necesita una **ruta de importación** con dos componentes: `archivo:objeto`. En este caso, `wsgi:app`.

!!! tip "Para qué sirve la PoC"
    La desplegaremos **por completo** (entorno virtual, servicio `systemd`, virtual host de Nginx, resolución de nombres) para que veas cada pieza por separado, sin ruido.

    Después repetiremos el mismo procedimiento con la aplicación real, donde **todo será más realista**: la estructura del proyecto, un `requirements.txt`, un mapa que consume una API externa y varios servicios conviviendo en el mismo servidor.

### 6.2. Aplicación real: records de atletismo

La segunda aplicación la hemos escrito para esta práctica y está publicada en:

[https://github.com/raul-profesor/atletismo-records](https://github.com/raul-profesor/atletismo-records)

La clonaremos en el [Paso 13](#paso-13-clonar-el-repositorio).

#### Qué hace

La aplicación muestra los **records mundiales vigentes de medio fondo y fondo de atletismo**, indicando **dónde y cuándo** se consequieron, mediante un mapa interactivo.

Incluye:

- Un **mapa interactivo** (Leaflet + OpenStreetMap) con un marcador por recinto, cuyo tamaño es proporcional a la altitud del terreno.
- Una **tabla filtrable** por categoría, sexo, modalidad y texto libre.
- Una **API JSON** (`/api/records`, `/api/recintos`, `/api/altitud`).
- Una **sonda de salud** en `/health`, pensada para engancharla a `systemd` o a un monitor de despliegue.

#### Por qué esta aplicación

Elegida por un motivo muy concreto: **los records de atletismo dependen del terreno**.

Una marca no es sólo un tiempo: es un tiempo *en un lugar*. El maratón de Londres (16 m sobre el nivel del mar) y el de Chicago (181 m) no son comparables entre sí, y los records de altura de los años 80 y 90 se batieron en circuitos con desnivel y en altitud. La altitud del recinto es, por tanto, **una variable de primer orden** para entender el rendimiento, y eso hace que un mapa que muestre la altitud de cada recinto sea algo informativo y no un adorno.

Además, la aplicación tiene una estructura realista: separa los datos (`app/datos.py`), el acceso a servicios externos (`app/elevacion.py`), las rutas (`app/__init__.py`) y las plantillas, e incorpora **degradación elegante** (si la API de altitud no responde, la aplicación sigue funcionando).

#### Estructura del proyecto

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

!!! note "Los datos"
    El fichero `data/records.json` contiene 19 records en 12 recintos, con las coordenadas y la altitud estimada de cada uno. Los datos proceden de [World Athletics](https://worldathletics.org/records) y están fechados, por lo que conviene revisarlos antes de cada curso.

    La **altitud exacta** de cada recinto no está en el JSON: se consulta en tiempo de ejecución a la [API de elevación de Open-Meteo](https://open-meteo.com/en/docs/elevation-api), que usa el modelo digital de elevación Copernicus GLO-90. El JSON sólo lleva una estimación de referencia.

---

## 7. Preparación del servidor

Todos los comandos de esta sección deben ejecutarse desde una terminal con permisos de administración.

### Paso 1: Actualizar el sistema e instalar el software necesario

Lo primero que hay que hacer **siempre** antes de instalar nada es actualizar los índices de paquetes y los propios paquetes del sistema. Esto garantiza que se instalan las últimas versiones disponibles y con sus parches de seguridad.

```bash
sudo apt update
sudo apt upgrade -y
```

Comprobamos las versiones del sistema y de las herramientas que vamos a necesitar:

```bash
cat /etc/os-release
python3 --version
git --version
nginx -v
```

Si no están instalados Python, Git o Nginx, los instalamos:

```bash
sudo apt install -y python3 python3-venv python3-pip git nginx
```

!!! note "Qué aporta cada paquete"
    - `python3`: el intérprete de Python.
    - `python3-venv`: el módulo `venv`, necesario para crear entornos virtuales con `python -m venv` (y usado internamente por `uv venv`).
    - `python3-pip`: el gestor de paquetes clásico, por si necesitas instalarlo en el sistema.
    - `git`: para clonar el repositorio de la aplicación real.

### Paso 2: Crear un usuario de servicio dedicado

!!! warning "Nunca ejecutes la aplicación como `root`"
    Tampoco como tu usuario personal. El enunciado original de esta práctica usaba `chown -R $USER:www-data /var/www/mi_aplicacion`, es decir, la aplicación se ejecutaba con los permisos de tu usuario de trabajo. Eso significa que **si un alumno de tu clase encuentra una vulnerabilidad de ejecución remota en tu aplicación, consigue un shell en el servidor con tus privilegios**, incluyendo tu clave SSH y tu acceso a `sudo`.

    La práctica correcta es crear un **usuario de sistema**, sin shell y sin directorio home utilizable, que sólo pueda leer y ejecutar lo mínimo necesario.

Creamos el usuario:

```bash
sudo useradd \
    --system \
    --home /opt/flask \
    --shell /usr/sbin/nologin \
    --user-group \
    flask
```

Verificamos su creación:

```bash
id flask
```

!!! info "Qué hace cada flag"
    | Flag | Significado |
    |---|---|
    | `--system` | Crea una **cuenta de sistema** (UID bajo 1000), sin shell interactivo ni contraseña asignada |
    | `--home /opt/flask` | Su directorio home (no se crea si no existe, pero lo usaremos como raíz de las apps) |
    | `--shell /usr/sbin/nologin` | Impide que nadie pueda abrir una sesión interactiva con este usuario |
    | `--user-group` | Crea además un grupo `flask` con el mismo nombre |

!!! note "Por qué NO `/var/www` y SÍ `/opt/flask`"
    `/var/www` es la raíz de documentos por defecto de Apache, y muchos servidores web sirven su contenido estático directamente desde ahí. `/opt` es la convención para software de terceros instalado y gestionado por el administrador del sistema. Como nuestra aplicación no se sirve de forma estática sino a través de un proxy inverso, `/opt/flask` es el sitio más limpio. Además, el directorio `www-data` del grupo `www-data` deja de ser relevante: **Nginx no necesita leer nada de nuestra aplicación**, solo mantener una conexión con Gunicorn.

### Paso 3: Crear la estructura de directorios

Creamos el árbol de directorios y lo ponemos en manos del usuario del servicio:

```bash
sudo mkdir -p /opt/flask/apps/mi_app /opt/flask/apps/atletismo
sudo chown -R flask:flask /opt/flask
```

Comprobamos los permisos:

```bash
ls -la /opt/flask/apps/
```

```text
drwxr-xr-x 2 flask flask 4096 ... atletismo
drwxr-xr-x 2 flask flask 4096 ... mi_app
```

!!! danger "Este paso no es opcional"
    Los dos directorios de proyecto **tienen que existir y tener como propietario a `flask`** antes de crear el entorno virtual.

    Si el directorio no existe, el `cd` del [Paso 5](#paso-5-crear-el-entorno-virtual-e-instalar-dependencias) fallará. Y si existe pero es de `root` (por ejemplo, si lo creaste con `sudo mkdir` sin luego hacer el `chown`), el `uv venv` fallará al intentar crear el `.venv` dentro:

    ```text
    error: Failed to create virtual environment
      cause: failed to create directory `.venv`: Permission denied (os error 13)
    ```

    !!! tip "El error engaña un poco"
        Dice "Permission denied" sobre `.venv`, pero el directorio `.venv` **no existe todavía**: lo que falla es crear el directorio dentro de `mi_app`, que pertenece a `root` y en el que `flask` no puede escribir.

        La solución no es dar permisos al `.venv` (que no existe), sino **arreglar el propietario del directorio padre**:

        ```bash
        sudo chown -R flask:flask /opt/flask
        ```

La estructura final será:

```text
/opt/flask/
└── apps/
    ├── mi_app/          <- Aplicación PoC
    │   ├── .venv/       <- Entorno virtual con uv
    │   ├── application.py
    │   ├── wsgi.py
    │   └── requirements.txt
    └── atletismo/       <- Aplicación real (clonada del repositorio)
        ├── .venv/
        ├── app/
        │   ├── __init__.py
        │   ├── datos.py
        │   ├── elevacion.py
        │   ├── templates/
        │   └── static/
        ├── data/
        │   └── records.json
        ├── wsgi.py
        └── requirements.txt
```

!!! tip "El directorio `.venv` va dentro del proyecto"
    Es una convención que `uv` sigue automáticamente: `uv pip install` busca un `.venv` en el directorio actual o en el padre más cercano. Si el entorno virtual vive en otro sitio, hay que tirar de `--python /ruta/al/entorno/bin/python` en cada comando. Dentro del proyecto, todo funciona sin configuración previa.

---

## 8. Gestión de dependencias con `uv`

### Paso 4: Instalar `uv`

Comprobamos si `uv` ya está disponible en el servidor:

```bash
command -v uv && uv --version
```

Si el comando muestra una ruta y una versión, ya lo tienes instalado. Aun así, te recomendamos reinstalarlo en `/usr/local/bin` (siguiente apartado), porque `uv` instalado en tu `home` **no funciona con `sudo -u flask`**. Si prefieres no reinstalarlo, el apartado [Instalar `uv` sin permisos de administrador](#instalar-uv-sin-permisos-de-administrador) te explica cómo resolverlo.

!!! danger "Por qué `uv` debe instalarse en `/usr/local/bin`"
    Hay **dos** obstáculos entre tú y un `uv` instalado en tu `home`, y los dos dan error:

    **1. El `PATH` de `sudo`.** Desde la versión 1.9.16, `sudo` tiene activa la opción `secure_path` por defecto:

    ```text
    Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    ```

    Esta opción **sustituye** tu `PATH` por una lista de directorios del sistema. El script de instalación deja `uv` en `~/.local/bin`, que no está en la lista, así que:

    ```text
    sudo -u flask uv venv
    # sudo: uv: command not found
    ```

    **2. Los permisos de tu directorio `home`.** Aunque indiques la ruta completa, el usuario `flask` tiene que **atravesar** tu `home` para llegar al binario. Y el `home` de un usuario creado por `cloud-init` (como el de una máquina virtual en la nube) suele tener permisos `700`:

    ```text
    drwx------ 20 ubuntu ubuntu 4096 /home/ubuntu
    ```

    Para un usuario sin permiso sobre ese directorio, el resultado es:

    ```text
    sudo -u flask /home/ubuntu/.local/bin/uv venv
    # sudo: unable to execute /home/ubuntu/.local/bin/uv: Permission denied
    ```

    !!! note "El error dice "Permission denied", no "No such file""
        Esto confunde a menudo: el fichero **sí** existe y **sí** tiene permisos de ejecución (`755`). Lo que falta es permiso para **recorrer** los directorios intermedios. En Unix, para ejecutar un binario necesitas permiso `x` (recorrido) en **todos** los directorios de la ruta, y `r-x` en el propio binario.

Instalamos `uv` en `/usr/local/bin`, que es un directorio del sistema, con permisos `755` y **sin** el problema del `home`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh
```

Verificamos la instalación:

```bash
/usr/local/bin/uv --version
```

```text
uv 0.13.7 (x86_64-unknown-linux-gnu)
```

!!! tip "Ahora sí funciona con `sudo`"
    Como `/usr/local/bin` está en el `secure_path` de `sudo` y es legible por todos los usuarios, estos comandos ya funcionan sin más complicaciones:

    ```bash
    sudo -u flask uv venv --python 3.12
    sudo -u flask uv pip install flask gunicorn
    ```

    Y no necesitas ninguna variable de shell.

!!! info "La variable de entorno `UV_INSTALL_DIR`"
    El script de instalación de `uv` permite elegir el directorio destino con esta variable. Sin ella, instala en `~/.local/bin`, que es lo que causa los problemas que acabamos de ver.

    !!! tip "Alternativa: el paquete de los repositorios"
        En Debian 13 (Trixie) y Ubuntu 25.04 o superiores, `uv` está disponible como paquete nativo y se instala directamente en `/usr/bin`:

        ```bash
        sudo apt update
        sudo apt install uv
        ```

        En versiones anteriores, el script de instalación instala una versión bastante más reciente, que es la opción preferible.

!!! warning "`uv` se instala en el home, no en el sistema"
    El binario queda en `~/.local/bin/uv`, que pertenece a **tu usuario**, no al usuario de servicio `flask`. Esto es intencional y no es un problema:

    - El ejecutable `gunicorn` que usará el servicio vive **dentro del entorno virtual** (`.venv/bin/gunicorn`), y es ese binario el que `systemd` invocará con su ruta absoluta.
    - `uv` sólo se usa en la fase de preparación, que ejecutas tú.

    !!! tip "Alternativa: instalarlo en el sistema"
        Si prefieres que `uv` esté disponible para **todos** los usuarios del servidor, incluido `root`, puedes instalarlo en `/usr/local/bin`, que sí está en el `secure_path` de `sudo`:

        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh
        ```

        En ese caso, `sudo -u flask uv ...` funciona directamente en los pasos siguientes, sin depender del `PATH` de tu usuario. Es la opción más cómoda si vas a desplegar varias aplicaciones.

#### Instalar `uv` sin permisos de administrador

Si no puedes escribir en `/usr/local/bin` (porque no tienes `sudo`, o por una política de la organización), hay una tercera vía: **copiar el binario al directorio del usuario del servicio**, que sí controlas:

```bash
sudo -u flask mkdir -p /opt/flask/bin
sudo -u flask cp "$(command -v uv)" /opt/flask/bin/uv
sudo -u flask chmod 755 /opt/flask/bin/uv
```

Y a partir de ahí, los comandos serían:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask /opt/flask/bin/uv venv --python 3.12
```

!!! note "¿Por qué esta vía funciona?"
    `/opt/flask` es el directorio que creamos en el [Paso 3](#paso-3-crear-la-estructura-de-directorios) y que pertenece al usuario `flask`. Al estar en su `home` efectivo, el usuario puede recorrerlo y ejecutar el binario sin problemas de permisos.

    Y al ser una ruta absoluta dentro de `/opt`, **tampoco** tiene nada que ver con el `secure_path` de `sudo`: funciona siempre.

!!! warning "El inconveniente de esta vía"
    El binario queda **copiado**, no instalado. Si más adelante actualizas `uv` en tu usuario, esta copia se queda atrás. Acuérdate de volver a copiarla.

### Paso 5: Crear el entorno virtual e instalar dependencias

Nos situamos en el directorio de la aplicación y creamos el entorno:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask uv venv --python 3.12
```

!!! info "¿Por qué `sudo -u flask`?"
    Para que el entorno virtual y los ficheros que se instalen en él pertenezcan al usuario del servicio, y no a tu usuario personal. Así, el servicio `systemd` podrá leerlos sin necesidad de permisos adicionales, y no habrá ficheros con permisos restringidos en `/opt/flask`.

    !!! tip "Lo que NO hay que hacer"
        No uses `sudo uv ...` sin `-u flask`. El comando se ejecutaría como `root` y el entorno virtual quedaría propiedad de `root`, no del usuario del servicio. El servicio `systemd` no podría escribir en él y tendrías que corregir permisos a mano.

    !!! note "¿Por qué `uv` y no `uv` con la ruta completa?"
        Como lo hemos instalado en `/usr/local/bin` (Paso 4), el nombre `uv` a secas ya funciona con `sudo`. Es más legible que repetir `/usr/local/bin/uv` en cada comando.

!!! note "`--python 3.12`"
    Si el servidor tiene esa versión de Python instalada, `uv` la usa. Si no, `uv` **la descarga automáticamente** (gestionada por `uv`), lo cual es muy cómodo en servidores donde no quieres tocar los repositorios del sistema.

Instalamos **Flask y Gunicorn**. Son los dos ejecutables que usaremos en el resto de la práctica:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask uv pip install flask gunicorn
```

!!! note "`flask` es el servidor de desarrollo, `gunicorn` el de producción"
    El paquete `flask` trae dos cosas: la biblioteca (el código de la aplicación) y el ejecutable `flask`, que es su **servidor de desarrollo**. El paquete `gunicorn` trae el ejecutable `gunicorn`, que es el **servidor de producción** que usaremos detrás de Nginx.

    Instalamos los dos aquí para no tener que volver a hacerlo más adelante.

Verificamos qué se ha instalado y dónde:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask uv pip list
ls -la .venv/bin/
```

!!! info "Los ejecutables viven en `.venv/bin/`"
    Fíjate en que aparecen `flask`, `gunicorn` y `python`. **Esta es la ruta que usaremos en la unidad de `systemd`**: `/opt/flask/apps/mi_app/.venv/bin/gunicorn`. Nunca usaremos simplemente `gunicorn`, porque el `PATH` del servicio systemd es distinto del de tu shell interactiva.

!!! tip "Un `requirements.txt` para poder recrear el entorno"
    Un entorno virtual es **descartable**: se borra y se recrea. Lo que no se puede perder es la lista de dependencias. La guardamos así:

    ```bash
    cd /opt/flask/apps/mi_app
    sudo -u flask uv pip freeze > requirements.txt
    ```

    Y para reconstruir el entorno en cualquier momento (o en otra máquina):

    ```bash
    uv venv && uv pip install -r requirements.txt
    ```

### Paso 6: Crear los ficheros de la aplicación

Dentro del directorio de la aplicación PoC:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask touch application.py wsgi.py
sudo chown flask:flask application.py wsgi.py
```

Editamos `application.py` y `wsgi.py` con el contenido del [apartado 6.1](#61-aplicacion-poc-proof-of-concept).

!!! tip "`touch` + `chown` en dos comandos"
    `touch` ejecutado con `sudo` crearía el fichero con `root` como propietario. El `chown` posterior corrige la propiedad. Alternativamente: `sudo -u flask touch application.py wsgi.py`.

---

## 9. Probar la aplicación en local

Antes de montar nada, conviene comprobar que la aplicación funciona. Veremos **dos** formas de ejecutarla y compararemos.

### Paso 7: Probar con el servidor de desarrollo de Flask

Usamos el ejecutable `flask` que instalamos en el [Paso 5](#paso-5-crear-el-entorno-virtual-e-instalar-dependencias). Lo arrancamos desde `wsgi.py`:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask .venv/bin/flask --app wsgi run --host 0.0.0.0 --port 5000
```

!!! info "¿Por qué `.venv/bin/flask` y no simplemente `flask`?"
    Dos razones:

    - **El entorno virtual está aislado.** El `flask` que tienes instalado en el sistema (si lo tienes) es otro distinto, y no tendría las dependencias de nuestra aplicación. Con la ruta completa, ejecutas el del venv.
    - **La ruta es relativa al directorio actual**, así que el comando anterior sólo funciona si estás en `/opt/flask/apps/mi_app`. Por eso el `cd` va siempre antes.

    !!! tip "El atajo `uv run`"
        `uv run` hace lo mismo eligiendo el venv por ti:

        ```bash
        cd /opt/flask/apps/mi_app
        sudo -u flask env PATH="$PATH" uv run flask --app wsgi run --host 0.0.0.0 --port 5000
        ```

        Es más corto, pero más opaco: si algo falla, no sabes con qué Python se está ejecutando. Para una práctica, la ruta completa es más fácil de depurar.

!!! note "Qué significa `--host 0.0.0.0`"
    Le indicamos al servidor que escuche en **todas** sus interfaces de red. Si lo dejamos en el valor por defecto (`127.0.0.1`), sólo aceptaría conexiones desde la propia máquina y no podríamos acceder desde el portátil.

Si preferimos usar el `if __name__ == "__main__": app.run()` que lleva `application.py`, el comando sería:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask .venv/bin/python application.py
```

!!! warning "Este servidor NO es apto para producción"
    El servidor de desarrollo de Flask:

    - **Usa un único proceso y un único hilo**: no atiende peticiones en paralelo.
    - **Dice explícitamente que no es estable** ni pensado para producción (su banner lo avisa).
    - **No reinicia los workers** si uno falla.
    - **No tiene ningún mecanismo de limitación** de peticiones, conexiones o recursos.
    - **No se integra con `systemd`** ni con la rotación de logs del sistema.

    Sirve para tu desarrollo local, punto. Lo que usaremos en producción es Gunicorn.

Comprobamos desde el navegador de nuestra máquina anfitriona: `http://IP-DEL-SERVIDOR:5000`

En la terminal del servidor, la salida del servidor de desarrollo debe parecerse a esto:

```text
 * Serving Flask app 'wsgi'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000
Press CTRL+C to quit
```

!!! warning "Fíjate en el aviso"
    El propio servidor de desarrollo te avisa de que **no es apto para producción**. No es un detalle: es la primera de las razones por las que en producción usaremos Gunicorn.

    Verás que responde a cada petición con una línea de log:

    ```text
    127.0.0.1 - - [08/Nov/2026:18:30:12] "GET / HTTP/1.1" 200 -
    ```

!!! tip "Recordatorio"
    Si no se conecta, comprueba el **grupo de seguridad** de la máquina virtual (en AWS, EC2 → Security Groups → Inbound Rules) y que el cortafuegos del sistema (`ufw`/`firewalld`) permite el puerto.

Detenemos el servidor con `CTRL+C`.

### Paso 8: Probar con Gunicorn en un puerto TCP

Ahora sí, con el servidor de producción:

```bash
cd /opt/flask/apps/mi_app
sudo -u flask .venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
```

Donde:

- `--workers 4` establece el número de procesos *worker*. La regla habitual de Gunicorn es **aproximadamente el doble de núcleos + 1** (`2 × nproc + 1`), porque los workers son de tipo *prefork* (bloqueantes) y no aprovechan la espera de E/S de la misma forma que un modelo asíncrono. Puedes ver los núcleos del servidor con `nproc`.

    !!! warning "No pongas demasiados workers"
        Cada worker es un proceso Python independiente con su propia copia de la aplicación. Si la aplicación es grande (por ejemplo, un ORM con modelos pesados), 20 workers pueden consumir cientos de megabytes. Empieza con `2 × nproc + 1` y mide.

- `--bind 0.0.0.0:5000` hace que el servidor escuche peticiones por todas sus interfaces de red y en el puerto 5000.

- `wsgi:app` es el nombre del archivo (sin extensión `.py`) y `app` es la instancia de la aplicación Flask dentro del archivo.

!!! info "La sintaxis `módulo:objeto`"
    Gunicorn resuelve `wsgi:app` así: importa el módulo `wsgi` y busca en él un atributo llamado `app`. Como `wsgi.py` hace `from application import app`, ese atributo es exactamente el objeto Flask, que es un *callable* WSGI válido.

Comprobamos de nuevo desde el navegador: `http://IP-DEL-SERVIDOR:5000`

Ahora la salida del servidor es la de Gunicorn, que **sí** es un servidor de producción:

```text
[2026-11-08 18:30:12 +0100] [12345] [INFO] Starting gunicorn 26.2.0
[2026-11-08 18:30:12 +0100] [12345] [INFO] Listening at: http://0.0.0.0:5000 (12345)
[2026-11-08 18:30:12 +0100] [12345] [INFO] Using worker: sync
[2026-11-08 18:30:12 +0100] [12346] [INFO] Booting worker with pid: 12346
[2026-11-08 18:30:12 +0100] [12347] [INFO] Booting worker with pid: 12347
[2026-11-08 18:30:12 +0100] [12348] [INFO] Booting worker with pid: 12348
[2026-11-08 18:30:12 +0100] [12349] [INFO] Booting worker with pid: 12349
```

!!! info "Lo que nos dice esta salida"
    - `Listening at: http://0.0.0.0:5000`: el proceso *master* ha abierto el puerto.
    - `Using worker: sync`: cada worker atiende las peticiones de forma **bloqueante** (es el tipo por defecto).
    - **Cuatro** líneas `Booting worker`: una por cada worker, con su PID. Estos son los que se van a reiniciar solos si uno falla.

Detenemos Gunicorn con `CTRL+C`.

### Paso 9: Convertir Gunicorn en un servicio de `systemd`

Hasta aquí todo era manual. En producción queremos que la aplicación:

- Arranque sola cuando el servidor se enciende.
- Se reinicie sola si se cuelga o si alguien la mata.
- Se pueda consultar y depurar con herramientas estándar del sistema.

Para eso creamos una **unidad de servicio de `systemd`**.

#### Decidir el directorio del socket Unix

Antes de escribir la unidad, tenemos que decidir **dónde vivirá el socket Unix** que usará Nginx para hablar con Gunicorn. Hay dos opciones habituales:

| Opción | Ruta | Ventaja | Inconveniente |
|---|---|---|---|
| Dentro del proyecto | `/opt/flask/apps/mi_app/mi_app.sock` | Path obvious | Hay que crearlo y borrarlo a mano; permisos heredados del directorio |
| Directorio de runtime | `/run/flask/mi_app.sock` | systemd lo crea y lo limpia solo, con el usuario correcto | Hay que declararlo en la unidad |

Vamos a usar la **segunda opción**, que es la que se usa en producción. `systemd` tiene una directiva `RuntimeDirectory` que:

1. Crea el directorio `/run/flask` al arrancar el servicio.
2. Le asigna como propietario al usuario del servicio (`flask`).
3. Lo elimina al parar el servicio.

Además, las rutas de socket Unix están limitadas a unos 100 bytes (el campo `sun_path` del protocolo `AF_UNIX`), así que conviene que sean cortas.

#### Escribir la unidad de servicio

Creamos el fichero:

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Y escribimos:

```ini
[Unit]
Description=Mi aplicacion Flask servida por Gunicorn
After=network.target

[Service]
Type=simple
User=flask
Group=flask
WorkingDirectory=/opt/flask/apps/mi_app

# El PATH empieza por el venv, para que 'gunicorn' sea el del entorno virtual
Environment="PATH=/opt/flask/apps/mi_app/.venv/bin"

# Variables de entorno de la aplicacion (el '-' evita que falle si no existe)
EnvironmentFile=-/opt/flask/apps/mi_app/.env

ExecStart=/opt/flask/apps/mi_app/.venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/flask/mi_app.sock \
    --access-logfile - \
    --error-logfile - \
    --timeout 30 \
    --graceful-timeout 30 \
    wsgi:app

# Recarga sin downtime: HUP hace que Gunicorn reinicie los workers
ExecReload=/bin/kill -s HUP $MAINPID

Restart=always
RestartSec=5
KillSignal=SIGQUIT
TimeoutStopSec=30

# Directorio de runtime: /run/flask, con el usuario del servicio
RuntimeDirectory=flask
RuntimeDirectoryMode=0750

# Hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
RestrictNamespaces=true
LockPersonality=true

[Install]
WantedBy=multi-user.target
```

!!! info "Qué hace cada directiva"
    | Directiva | Función |
    |---|---|
    | `After=network.target` | Arranca **después** de que la red esté lista |
    | `Type=simple` | El proceso principal es el propio Gunicorn (no un script de arranque) |
    | `User` / `Group` | Identidad con la que se ejecuta la aplicación: **nunca root** |
    | `WorkingDirectory` | Directorio desde el que se ejecuta Gunicorn (donde están las plantillas y `static/`) |
    | `Environment="PATH=..."` | Pone el venv **al principio** del `PATH` |
    | `EnvironmentFile=-...` | Carga las variables del `.env`. El prefijo `-` indica que el fichero es opcional |
    | `ExecStart` | El comando de arranque, con la **ruta absoluta** al ejecutable |
    | `--bind unix:...` | **Crea el socket Unix** que Nginx consumirá. Este es el detalle que faltaba en el enunciado original |
    | `--access-logfile -` | Los logs de acceso van a `stdout`, que systemd captura en el journal |
    | `--error-logfile -` | Ídem para los errores |
    | `--timeout 30` | Si un worker tarda más de 30 s en responder, se le mata y se reinicia |
    | `ExecReload` + `HUP` | Recarga los workers sin tumbar el servicio |
    | `Restart=always` | Si el proceso muere, systemd lo vuelve a arrancar |
    | `RestartSec=5` | Espera 5 s entre reinicios, para no entrar en un bucle |
    | `KillSignal=SIGQUIT` | Al parar, Gunicorn termina los workers de forma ordenada |
    | `TimeoutStopSec=30` | Margen para que los workers terminen las peticiones en curso |
    | `RuntimeDirectory` | systemd crea `/run/flask` con el usuario correcto y lo limpia al parar |

!!! warning "El bloque de hardening no es decorativo"
    `ProtectSystem=strict` hace que todo el sistema de ficheros sea de **sólo lectura** para el servicio, salvo las rutas declaradas en `ReadWritePaths`. `ProtectHome=true` impide que el servicio lea tu `/home`. `PrivateTmp=true` le da su propio `/tmp` aislado. `NoNewPrivileges=true` impide que el proceso gane privilegios mediante `setuid`.

    Todo esto limita mucho el daño si un alumno (o un atacante) consigue ejecutar código dentro de la aplicación. Es la diferencia entre "la aplicación corría como root" y "la aplicación corre como un usuario sin acceso a nada".

!!! note "El `.env` de la aplicación"
    Creamos el fichero de variables de entorno:

    ```bash
    sudo -u flask touch /opt/flask/apps/mi_app/.env
    sudo -u flask nano /opt/flask/apps/mi_app/.env
    ```

    Contenido típico:

    ```text
    FLASK_APP=wsgi:app
    FLASK_ENV=production
    SECRET_KEY=una-clave-larga-y-aleatoria
    ```

    !!! danger "Nunca subas el `.env` al repositorio"
        El `.env` contiene secretos. Debe estar en el `.gitignore` y tener permisos restrictivos:

        ```bash
        sudo chmod 640 /opt/flask/apps/mi_app/.env
        ```

#### Habilitar y arrancar el servicio

Como cada vez que se crea un servicio nuevo de `systemd`, se habilita y se inicia:

```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
```

Comprobamos el estado:

```bash
sudo systemctl status flask-app
```

Deberías ver algo como:

```text
● flask-app.service - Mi aplicacion Flask servida por Gunicorn
     Loaded: loaded (/etc/systemd/system/flask-app.service; enabled)
     Active: active (running) since ...
   Main PID: 12345 (gunicorn)
      Tasks: 5 (limit: 38284)
     Memory: 62.4M
```

!!! info "Comprobaciones útiles"
    - `systemctl is-enabled flask-app` → `enabled`
    - `systemctl is-active flask-app` → `active`
    - `systemctl show -p MainPID flask-app` → el PID del proceso master
    - `ps -ef | grep gunicorn` → verás el master y sus 4 workers

#### Verificar que el socket se ha creado

Este es el punto que conviene comprobar **antes** de configurar Nginx:

```bash
ls -la /run/flask/
```

Deberías ver el socket:

```text
srwxr-xr-x 1 flask flask 0 Sep  8 10:23 /run/flask/mi_app.sock
```

Y podemos probar que Gunicorn responde a través del socket, sin pasar por Nginx:

```bash
sudo -u flask curl --unix-socket /run/flask/mi_app.sock http://localhost/
```

!!! warning "Este paso es la clave de la práctica"
    En el enunciado original, la configuración de Nginx apuntaba a un socket `unix:` que **nadie creaba nunca**. El alumno se encontraba con un `502 Bad Gateway` sin ninguna pista de por qué. Si haces esta comprobación, el error aparece en el minuto 20 y no en el minuto 45.

---

## 10. Nginx como proxy inverso

### Paso 10: Configurar el virtual host de Nginx

Creamos el fichero de configuración del sitio web:

```bash
sudo nano /etc/nginx/sites-available/flask-app
```

Y escribimos:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name flask-app.local www.flask-app.local;

    server_tokens off;
    client_max_body_size 10m;

    access_log /var/log/nginx/flask-app.access.log;
    error_log  /var/log/nginx/flask-app.error.log;

    # Los ficheros estaticos los sirve Nginx directamente, sin pasar por Gunicorn
    location /static/ {
        alias /opt/flask/apps/mi_app/static/;
        expires 30d;
        access_log off;
    }

    location / {
        include proxy_params;

        # Proxy inverso hacia el socket Unix de Gunicorn
        proxy_pass http://unix:/run/flask/mi_app.sock;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        proxy_connect_timeout 5s;
        proxy_read_timeout    60s;
    }
}
```

!!! info "Comentarios sobre la configuración"
    - **`server_name`**: los nombres de dominio que responderá este virtual host. Más adelante lo resolveremos con `/etc/hosts` (ver el [Paso 12](#paso-12-resolver-el-nombre-y-verificacion-final)).
    - **`access_log` / `error_log`**: los logs de acceso y de errores, en ficheros separados para poder analizarlos por separado.
    - **`server_tokens off`**: no revela la versión de Nginx en las cabeceras de respuesta. Es una medida básica de *hardening*.
    - **`location /static/`**: Nginx sirve directamente los ficheros estáticos de la aplicación, sin molestar a Gunicorn. Es una optimización importante: las CSS y las imágenes son las peticiones más frecuentes, y no requieren ejecutar Python.
    - **`proxy_pass http://unix:/ruta/al/socket`**: el proxy inverso hacia Gunicorn.

!!! warning "El detalle de la barra final en `proxy_pass`"
    Si escribimos `proxy_pass http://unix:/run/flask/mi_app.sock;` **sin barra final**, Nginx reenvía la URI original sin modificarla. Si le añadimos una barra final (`.../socket/`), Nginx **elimina el prefijo** de la URI antes de reenviarla, y las rutas de la aplicación dejarán de funcionar. Es un clásico.

!!! tip "Variante con TCP en lugar de socket Unix"
    Si prefieres la versión con puerto (más fácil de depurar con `curl http://127.0.0.1:8000`), el `ExecStart` del servicio sería:

    ```ini
    ExecStart=/opt/flask/apps/mi_app/.venv/bin/gunicorn \
        --workers 4 \
        --bind 127.0.0.1:8000 \
        wsgi:app
    ```

    y en Nginx:

    ```nginx
    proxy_pass http://127.0.0.1:8000;
    ```

    El socket Unix es preferible porque no abre un puerto (aunque sea en `localhost`) y se comporta mejor con muchos workers.

### Paso 11: Habilitar el sitio y recargar Nginx

Creamos el enlace simbólico del sitio disponible al de sitios activos:

```bash
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
```

Y nos aseguramos de que se ha creado dicho enlace simbólico:

```bash
ls -l /etc/nginx/sites-enabled/ | grep flask-app
```

!!! note "El directorio `sites-available` frente a `sites-enabled`"
    Es una convención de Debian y Ubuntu. `sites-available` contiene todas las configuraciones posibles; `sites-enabled` contiene los enlaces simbólicos a las que Nginx realmente dará servicio. Así se activa o desactiva un sitio con un simple `ln -s` o `rm`, sin tocar el fichero de configuración.

Comprobamos que la configuración de Nginx no contiene errores:

```bash
sudo nginx -t
```

Debería mostrar:

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

!!! warning "Comprueba siempre con `nginx -t` antes de recargar"
    Si hay un error de sintaxis y recargas igualmente, **te quedas sin servidor web**: Nginx se queda con la configuración anterior, pero si el error impide la carga, el servicio no arranca. Con `nginx -t` lo sabrás antes de tocar nada.

Recargamos Nginx y comprobamos su estado:

```bash
sudo systemctl reload nginx
sudo systemctl status nginx
```

!!! info "`reload` frente a `restart`"
    `reload` pide a Nginx que **recargue la configuración sin tumbar las conexiones existentes**. Es la forma correcta de aplicar cambios: los usuarios conectados no notan nada.

### Paso 12: Resolver el nombre y verificación final

En este momento, la aplicación ya es accesible por IP:

```bash
curl -i http://IP-DEL-SERVIDOR/
```

Pero queremos acceder por nombre de dominio, que es como se hará en producción.

!!! note "Recordemos que aún no hemos tratado con el DNS"
    El tema 4 del curso está dedicado al DNS. Por ahora, la forma más sencilla de resolver el nombre es editar el fichero `hosts` de nuestra **máquina anfitriona** (la del portátil, no el servidor).

En Linux y macOS, el fichero está en:

```text
/etc/hosts
```

En Windows:

```text
C:\Windows\System32\drivers\etc\hosts
```

Añadimos una línea:

```text
192.168.X.X flask-app.local www.flask-app.local
```

donde `192.168.X.X` es la IP de tu máquina virtual.

!!! warning "No edites `/etc/hosts` del servidor para esto"
    Si editas el `/etc/hosts` **del servidor**, la resolución funciona sólo dentro del servidor, no desde tu portátil. Necesitas editar el fichero de tu máquina local. Puedes editar el del servidor con `sudo nano /etc/hosts` y necesitas permisos de administrador en Windows (hay que abrir el Bloc de notas como administrador o usar PowerShell con permisos elevados).

Comprobamos que la resolución funciona:

```bash
ping flask-app.local
```

Y por fin, la prueba final desde el navegador de la máquina anfitriona:

```text
http://flask-app.local
```

Deberíamos ver la misma página que en el [Paso 8](#paso-8-probar-con-gunicorn-en-un-puerto-tcp).

Podemos verificarlo también desde el terminal, que es más cómodo para documentar:

```bash
curl -i http://flask-app.local/
```

```text
HTTP/1.1 200 OK
Server: nginx
Date: Sun, 08 Nov 2026 18:32:07 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 69
Connection: keep-alive

<h1>Mi aplicacion Flask</h1><p>Desplegada con Nginx + Gunicorn</p>
```

!!! info "Las cabeceras de la respuesta"
    Fíjate en `Server: nginx`: la respuesta la ha compuesto Nginx, no Gunicorn. Y en que **no** aparece ninguna cabecera `Server: gunicorn`, porque Nginx la sustituye. Por eso el `server_tokens off` que pusimos en la configuración es una medida útil: sin él, la respuesta habría revelado la versión exacta de Nginx.

!!! success "¡Despliegue completado!"
    Ya tenemos una aplicación Flask servida por Gunicorn, gestionada por `systemd` y publicada a través de Nginx. Y todo ello con un usuario sin privilegios, un socket Unix y un despliegue reproducible con `uv`.

---

## 11. Desplegar la aplicación real de atletismo

Ya hemos desplegado la PoC. Ahora repetimos el procedimiento con la aplicación real, que es donde el despliegue se pone interesante.

### Paso 13: Clonar el repositorio

```bash
cd /opt/flask/apps
sudo -u flask git clone https://github.com/raul-profesor/atletismo-records atletismo
cd atletismo
ls -la
```

!!! note "La propiedad de los ficheros"
    Como clonamos con `sudo -u flask`, todo el contenido pertenece al usuario `flask`, que es el que ejecutará el servicio.

### Paso 14: Crear el entorno e instalar las dependencias

Esta aplicación sí trae un `requirements.txt` correcto y actualizado, así que la instalación es distinta de la de la PoC:

```bash
cd /opt/flask/apps/atletismo
sudo -u flask uv venv --python 3.12
sudo -u flask uv pip install -r requirements.txt
```

!!! note "El `requirements.txt` incluye Flask y Gunicorn"
    Su contenido es:

    ```text
    Flask==3.1.3
    Werkzeug==3.1.3
    gunicorn==26.2.0
    ```

    Es decir, `pip install -r requirements.txt` instala **los dos ejecutables** que vamos a usar (`flask` y `gunicorn`), igual que los instalamos a mano en la PoC. La diferencia es que aquí las versiones están fijadas y declaradas en un fichero, que es lo que hace un despliegue reproducible.

Comprobamos qué se ha instalado:

```bash
cd /opt/flask/apps/atletismo
sudo -u flask uv pip list
ls -la .venv/bin/
```

!!! warning "Un detalle de `uv` que puede confundir"
    `uv pip` **busca hacia arriba** un `pyproject.toml` y, si encuentra uno, instala en el entorno virtual de ese proyecto en lugar del tuyo. Si tu servidor tiene un `pyproject.toml` en un directorio padre, las dependencias se irían allí.

    Para forzar el entorno correcto, indica la variable `VIRTUAL_ENV`:

    ```bash
    cd /opt/flask/apps/atletismo
    sudo -u flask env VIRTUAL_ENV="$PWD/.venv" uv pip install -r requirements.txt
    ```

    Comprobamos que el entorno es el correcto:

    ```bash
    cd /opt/flask/apps/atletismo
    sudo -u flask .venv/bin/python -c "import flask; print('Flask OK')"
    ```

### Paso 15: Probar la aplicación en local

Primero con el servidor de desarrollo, para verificar que todo funciona:

```bash
cd /opt/flask/apps/atletismo
sudo -u flask .venv/bin/flask --app wsgi run --host 0.0.0.0 --port 5000
```

Comprobamos en el navegador que:

- Se ve el mapa con los marcadores de los recintos.
- La tabla muestra los 19 records.
- Los filtros funcionan (por ejemplo, elegir «Fondo» o buscar «Monaco»).
- El formulario de búsqueda devuelve resultados.

!!! info "Comprueba también la sonda de salud"
    En otra terminal:

    ```bash
    curl -s http://127.0.0.1:5000/health
    ```

    Debe devolver algo como:

    ```json
    {"estado": "ok", "records": 19}
    ```

    !!! warning "Un detalle importante sobre la API de altitud"
        La aplicación consulta la altitud del terreno a la API de Open-Meteo **en tiempo de ejecución**. Si el servidor no tiene salida a Internet, la aplicación **no se rompe**: registra un aviso en el log y muestra la altitud estimada que viene en el JSON.

Detenemos el servidor con `CTRL+C` y probamos con Gunicorn:

```bash
cd /opt/flask/apps/atletismo
sudo -u flask .venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
```

!!! tip "El punto de entrada vuelve a ser `wsgi:app`"
    El comando es idéntico al de la PoC: la estructura del proyecto no cambia el punto de entrada, siempre que respetemos la convención `archivo:objeto`.

### Paso 16: Crear el servicio systemd de la aplicación real

Como esta aplicación tiene su propio directorio, su propio entorno virtual y su propio socket, necesita **su propio servicio** y **su propio virtual host**.

```bash
sudo nano /etc/systemd/system/flask-atletismo.service
```

```ini
[Unit]
Description=Records de atletismo (Flask + Gunicorn)
After=network.target

[Service]
Type=simple
User=flask
Group=flask
WorkingDirectory=/opt/flask/apps/atletismo
Environment="PATH=/opt/flask/apps/atletismo/.venv/bin"
EnvironmentFile=-/opt/flask/apps/atletismo/.env
ExecStart=/opt/flask/apps/atletismo/.venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/flask/atletismo.sock \
    --access-logfile - \
    --error-logfile - \
    --timeout 30 \
    --graceful-timeout 30 \
    wsgi:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5
KillSignal=SIGQUIT
TimeoutStopSec=30
RuntimeDirectory=flask
RuntimeDirectoryMode=0750
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
RestrictNamespaces=true
LockPersonality=true

[Install]
WantedBy=multi-user.target
```

!!! note "Las diferencias con el servicio de la PoC"
    Sólo cambian **cuatro** líneas:

    1. `WorkingDirectory`: apunta a `atletismo`.
    2. `Environment="PATH=..."`: apunta al venv de `atletismo`.
    3. `ExecStart`: usa el ejecutable de `atletismo` y el socket `atletismo.sock`.
    4. La `Description` describe la aplicación.

    Y como los dos servicios comparten `RuntimeDirectory=flask`, ambos conviven sin problema: cada uno crea su socket con un nombre distinto dentro del mismo directorio.

Arrancamos el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-atletismo
sudo systemctl start flask-atletismo
sudo systemctl status flask-atletismo
```

!!! info "Comprobación de los sockets"
    Ahora debe haber **dos** sockets, uno por aplicación:

    ```bash
    ls -la /run/flask/
    ```

    ```text
    srwxr-xr-x 1 flask flask 0 ... /run/flask/atletismo.sock
    srwxr-xr-x 1 flask flask 0 ... /run/flask/mi_app.sock
    ```

    Y podemos probar cada uno por separado, sin pasar por Nginx:

    ```bash
    sudo -u flask curl --unix-socket /run/flask/atletismo.sock http://localhost/health
    ```

### Paso 17: Configurar el virtual host de Nginx

```bash
sudo nano /etc/nginx/sites-available/flask-atletismo
```

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name atletismo.local www.atletismo.local;

    server_tokens off;
    client_max_body_size 10m;

    access_log /var/log/nginx/flask-atletismo.access.log;
    error_log  /var/log/nginx/flask-atletismo.error.log;

    # Los ficheros estaticos los sirve Nginx directamente, sin pasar por Gunicorn
    location /static/ {
        alias /opt/flask/apps/atletismo/app/static/;
        expires 30d;
        access_log off;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/flask/atletismo.sock;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        proxy_connect_timeout 5s;
        proxy_read_timeout    60s;
    }
}
```

!!! info "Ojo con la ruta del `alias`"
    Los ficheros estáticos de esta aplicación están en `app/static/`, no en `static/`. Es un detalle fácil de equivocar: si el `alias` apunta a un directorio inexistente, Nginx devuelve **404** en todos los CSS y las imágenes, y la página se ve sin estilos.

    Compruébalo antes de recargar:

    ```bash
    ls -la /opt/flask/apps/atletismo/app/static/css/
    ```

!!! warning "Las cabeceras `X-Forwarded-*` no son un adorno"
    Esta aplicación (y cualquier otra) necesita saber cuál era la URL original y el protocolo de la petición. Sin esas cabeceras, `url_for()` generaría URLs con `http://` en lugar de `https://` y las redirecciones se irían al sitio equivocado. Con un proxy inverso delante, **el backend nunca ve la petición original**: sólo ve la conexión con Nginx.

Habilitamos el sitio y recargamos:

```bash
sudo ln -s /etc/nginx/sites-available/flask-atletismo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

!!! tip "Comprobación desde el propio servidor"
    Antes de salir a la máquina local, comprueba que Nginx responde:

    ```bash
    curl -i -H "Host: atletismo.local" http://127.0.0.1/
    ```

    Si devuelve `200 OK` y el HTML de la página, el despliegue está correcto y lo único que falta es la resolución del nombre en tu máquina.

Añadimos la resolución del nombre en el `/etc/hosts` de nuestra máquina local:

```text
192.168.X.X atletismo.local www.atletismo.local
```

Y comprobamos desde el navegador:

```text
http://atletismo.local
```

!!! success "Segunda aplicación desplegada"
    Ya tenemos las dos aplicaciones funcionando de forma simultánea, cada una con su propio servicio, su propio socket y su propio virtual host, compartiendo la misma instalación de Nginx.

    Y ahora tenemos algo mejor que un "Hello World": una aplicación que **consulta datos de una API externa**, sirve un mapa interactivo, y se degrada con elegancia cuando esa API no responde.

---

## 12. Comparativa: PoC vs aplicación real

| Aspecto | PoC (`mi_app`) | Aplicación real (`atletismo`) |
|---|---|---|
| Origen | Ficheros creados a mano | Repositorio Git clonado |
| Punto de entrada | `wsgi.py` → `wsgi:app` | `wsgi.py` → `wsgi:app` |
| Dependencias | Instaladas con `uv pip install` | `requirements.txt` + `uv pip install -r` |
| Estructura | Dos ficheros sueltos | Paquete `app/` con datos, API y vistas separados |
| Datos | En el código | Fichero `data/records.json` |
| Ficheros estáticos | No hay | CSS y JavaScript del mapa |
| Plantillas | HTML en línea | Jinja2 (`index.html`) |
| Rutas | Una (`/`) | Cinco (`/`, `/api/records`, `/api/recintos`, `/api/altitud`, `/health`) |
| Dependencias externas | Ninguna | API de elevación de Open-Meteo |
| Servicio systemd | `flask-app.service` | `flask-atletismo.service` |
| Socket | `/run/flask/mi_app.sock` | `/run/flask/atletismo.sock` |
| Virtual host | `flask-app.local` | `atletismo.local` |
| Código a escribir | `application.py` + `wsgi.py` | Ninguno (ya está en el repo) |

!!! note "Qué conviene observar"
    Aunque el procedimiento es el mismo, **cada paso tiene su propio detalle**: el `WorkingDirectory` y el `PATH` cambian, el socket tiene otro nombre, y la ruta de los ficheros estáticos está un nivel más profunda (`app/static/` en lugar de `static/`).

    **Este es el motivo por el que las variables están separadas en la unidad de servicio y no escritas a fuego en un único fichero**: un despliegue real con muchas aplicaciones se parece más a esto.

!!! tip "El salto de la PoC a la aplicación real"
    La PoC sirve para entender cada pieza por separado. La aplicación real introduce dos cosas que no había: una **estructura de proyecto** en la que los datos y las vistas están separados del código, y una **dependencia de un servicio externo** que puede no estar disponible.

    Ambas cosas son el día a día de un despliegue real, y por eso la práctica insiste en una cosa: **no basta con instalar, hay que ejecutar y comprobar**.

---

## 13. Comandos de referencia rápida

### Python y `uv`

| Acción | Comando |
|---|---|
| Instalar `uv` en el sistema | `curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh` |
| Ver la versión | `uv --version` |
| Crear el entorno | `sudo -u flask uv venv --python 3.12` |
| Instalar paquetes | `sudo -u flask uv pip install flask gunicorn` |
| Crear el entorno virtual | `uv venv --python 3.12` |
| Crear el entorno con un Python concreto | `uv venv --python 3.13` |
| Instalar las dependencias | `uv pip install -r requirements.txt` |
| Instalar un paquete | `uv pip install flask gunicorn` |
| Ver lo instalado | `uv pip list` |
| Congelar dependencias | `uv pip freeze > requirements.txt` |
| Ejecutar en el entorno | `uv run gunicorn wsgi:app` |
| Alternativa con `venv` estándar | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` |

### Flask y Gunicorn

| Acción | Comando |
|---|---|
| Servidor de desarrollo | `.venv/bin/flask --app wsgi run --host 0.0.0.0 --port 5000` |
| Gunicorn con TCP | `.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app` |
| Gunicorn con socket Unix | `.venv/bin/gunicorn --workers 4 --bind unix:/run/flask/mi_app.sock wsgi:app` |
| Ver el número de cores | `nproc` |
| Workers recomendados | `2 × nproc + 1` |
| Probar el socket a mano | `curl --unix-socket /run/flask/mi_app.sock http://localhost/` |
| Ver los workers | `ps -ef \| grep gunicorn` |

### `systemd`

| Acción | Comando |
|---|---|
| Recargar los ficheros de unidad | `sudo systemctl daemon-reload` |
| Habilitar al arranque | `sudo systemctl enable flask-app` |
| Arrancar | `sudo systemctl start flask-app` |
| Parar | `sudo systemctl stop flask-app` |
| Reiniciar | `sudo systemctl restart flask-app` |
| Estado | `sudo systemctl status flask-app` |
| Logs en vivo | `sudo journalctl -u flask-app -f` |
| Logs de las últimas 100 líneas | `sudo journalctl -u flask-app -n 100 --no-pager` |
| Recarga sin downtime | `sudo systemctl reload flask-app` |
| Ver el PID principal | `systemctl show -p MainPID flask-app` |

### Nginx

| Acción | Comando |
|---|---|
| Test de configuración | `sudo nginx -t` |
| Recargar | `sudo systemctl reload nginx` |
| Estado | `sudo systemctl status nginx` |
| Logs de acceso | `sudo tail -f /var/log/nginx/flask-app.access.log` |
| Logs de error | `sudo tail -f /var/log/nginx/flask-app.error.log` |
| Habilitar un sitio | `sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/` |
| Ver los sitios activos | `ls -l /etc/nginx/sites-enabled/` |

---

## 14. Diagnóstico rápido

Los problemas están ordenados según el momento del despliegue en el que suelen aparecer.

### Entorno y dependencias

| Problema | Causa probable | Solución |
|---|---|---|
| `uv: command not found` | No está en el `PATH` | `export PATH="$HOME/.local/bin:$PATH"` y añade esa línea a `~/.bashrc` |
| `sudo: uv: command not found` | `sudo` sustituye el `PATH` por `secure_path` y `uv` está en `~/.local/bin` | Instala `uv` en `/usr/local/bin` (Paso 4) |
| `sudo: unable to execute .../uv: Permission denied` | El usuario `flask` no puede recorrer tu `home`, que tiene permisos `700` | Instala `uv` en `/usr/local/bin` (Paso 4) |
| `failed to create directory '.venv': Permission denied` | El directorio del proyecto es de `root`, así que `flask` no puede escribir dentro | `sudo chown -R flask:flask /opt/flask` (Paso 3) |
| `No virtual environment found` al instalar | El `uv venv` anterior falló y no creó el `.venv` | Arregla los permisos del directorio y repite el `uv venv` |
| `No virtual environment found` | No hay `.venv` en el directorio | `uv venv --python 3.12` |
| `AttributeError: module 'ast' has no attribute 'Str'` | `Werkzeug 2.2.2` usa una API de `ast` eliminada en Python 3.12 | Actualiza a `Flask>=3.1` y `Werkzeug>=3.1` |
| `ImportError: cannot import name 'url_quote' from 'werkzeug.urls'` | `Flask==2.0.2` con un `Werkzeug` 2.3 o superior | Actualiza a `Flask>=3.1` y `Werkzeug>=3.1` |
| `ModuleNotFoundError: No module named 'flask'` | Se ejecutó el Python del sistema, no el del venv | Usa `.venv/bin/python` o `.venv/bin/flask` |
| `error: externally-managed-environment` (pip) | Se intentó instalar en el Python del sistema | Instala siempre dentro del venv, o usa `uv pip` |

### Gunicorn

| Problema | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'wsgi'` | Se usó `wsgi:app` en el repo que sólo tiene `app.py` | Usa `app:app` |
| `ModuleNotFoundError: No module named 'app'` | Se usó `app:app` en un proyecto que sólo tiene `wsgi.py` | Usa `wsgi:app` |
| `Address already in use` | El puerto 5000 ya está ocupado | `ss -lntp \| grep 5000` para ver quién lo tiene |
| `Permission denied` al crear el socket | El directorio no pertenece al usuario del servicio | `RuntimeDirectory=flask` en la unidad, o revisa la propiedad de `/run/flask` |
| `WORKER TIMEOUT` en los logs | Un worker tarda más de `--timeout` segundos | Increase `--timeout` o revisa si hay consultas lentas a la base de datos |
| `Connection refused` al usar el socket | Gunicorn no está corriendo o el socket no existe | `systemctl status flask-app` y `ls -la /run/flask/` |

### Nginx

| Problema | 502 Bad Gateway | Causa: Gunicorn no está corriendo, o el path del socket es incorrecto. Solución: `sudo systemctl status flask-app`, `ls -la /run/flask/`, compara con `proxy_pass` |
| 502 Bad Gateway | La ruta de `proxy_pass` no coincide con el `--bind` | Un typo en un carácter y ya no funciona. Compara ambas cadenas |
| 404 Not Found | `proxy_pass` con barra final | Elimina la barra final: `proxy_pass http://unix:/run/flask/mi_app.sock;` |
| 403 Forbidden | Permisos de los ficheros estáticos | `sudo chown -R flask:flask /opt/flask/apps/atletismo/app/static` |
| 502 sólo después de recargar Nginx | Nginx se recargó antes de que Gunicorn creara el socket | `sudo systemctl restart flask-app` y luego `sudo systemctl reload nginx` |
| No se ven los estilos | `location /static/` con `alias` mal escrito | La ruta del `alias` debe terminar en `/` y coincidir con el directorio real |

### DNS y resolución de nombres

| Problema | Causa probable | Solución |
|---|---|---|
| `ERR_NAME_NOT_RESOLVED` | El `/etc/hosts` de la máquina local no tiene la línea | Edita el fichero de tu máquina **anfitriona**, no el del servidor |
| `ERR_CONNECTION_REFUSED` en el navegador | El puerto 80 está bloqueado por el cortafuegos o el grupo de seguridad | `sudo ufw allow 80/tcp` y revisa el grupo de seguridad de la VM |
| `ping` funciona pero el navegador no | Se editó el `/etc/hosts` equivocado | Recuerda: el del portátil, no el del servidor |

---

## 15. Cuestiones

!!! task "Cuestión 1"
    Busca, lee, entiende y explica qué es un **servidor WSGI** y para qué sirve. Compara WSGI con el protocolo CGI clásico y explica qué problema resuelve.

!!! task "Cuestión 2"
    ¿Por qué no debemos usar el servidor de desarrollo de Flask en producción? Enumera al menos cuatro razones y explica en qué momento de esta práctica lo hemos utilizado y con qué objetivo.

!!! task "Cuestión 3"
    ¿Qué diferencia hay entre WSGI y ASGI? ¿En qué casos conviene uno y en cuáles el otro? Investiga si Flask 3 es un framework WSGI o ASGI, y qué servidores se pueden usar en cada caso.

!!! task "Cuestión 4"
    ¿Cómo se dimensiona el número de workers de Gunicorn? Explica la regla `2 × cores + 1`, cuándo deja de ser válida, y qué tipo de worker (`sync`, `gthread`, `gevent`) convendría para una aplicación con muchas peticiones de E/S (por ejemplo, una que consulta una API externa).

!!! task "Cuestión 5"
    ¿Por qué en esta práctica usamos un socket Unix en lugar de un puerto TCP entre Nginx y Gunicorn? Enumera las ventajas y las desventajas. ¿En qué situación concreta sería preferible usar un puerto TCP?

!!! task "Cuestión 6"
    Explica la diferencia entre `pip`, `pipenv` y `uv`. ¿Por qué `pipenv` dejó de ser la herramienta de referencia? ¿Qué ventajas tiene `uv` frente a las otras dos?

---

## 16. Tarea de ampliación

!!! task "Ampliación"
    Realiza alguna de las siguientes mejoras sobre el despliegue que has construido. Cada una es independiente, así que puedes elegir la que más te interese.

    **A. Ajuste de rendimiento y medición**

    1. Instala una herramienta de carga como `hey` (o usa `ab`, que viene con el paquete `apache2-utils`) y mide el throughput de la aplicación con distintos números de workers (1, 2, 4, 8).
    2. Compara el rendimiento del socket Unix con el de un puerto TCP en `127.0.0.1`.
    3. Documenta en una tabla qué configuración da mejores resultados en tu servidor y **por qué**.

    **B. Monitorización a partir del health check**

    La aplicación de atletismo ya incluye la ruta `/health`. El trabajo ahora es conectarla al sistema:

    1. Configura un `Healthcheck` en la unidad de `systemd` o un script que compruebe esa ruta periódicamente con `curl` y reinicie el servicio si falla.
    2. Configura el envío de los logs de Gunicorn a un fichero con rotación mediante `logrotate`, en lugar de dejarlos sólo en el journal.
    3. Mide cuánto tarda la aplicación en responder a `/health` con `curl -w "%{time_total}"` y compáralo con el tiempo de respuesta de la página principal, que es más lenta porque consulta la API de altitud.

    **C. WSGI frente a ASGI**

    1. Despliega la misma aplicación con un servidor **ASGI** (Uvicorn o Hypercorn), usando el soporte asíncrono de Flask (`flask[async]`).
    2. Compara el comportamiento de ambos despliegues con la ruta `/api/altitud`, que hace una llamada de E/S a un servicio externo.
    3. Redacta una conclusión sobre cuándo compensa cada arquitectura.

    !!! tip "Una pista"
        La ruta `/api/altitud` es la candidata ideal para esta comparación: hace una llamada HTTP a un servidor externo y, por tanto, **espera**. Es exactamente el escenario en el que un modelo asíncrono puede mantener más conexiones abiertas con menos recursos.

    **D. Automatización del despliegue**

    1. Escribe un script de shell (`desplegar.sh`) que automatice todo el proceso: clonar, crear el venv, instalar dependencias, copiar la unidad de `systemd`, enlazar el virtual host, recargar Nginx y verificar el estado.
    2. Documenta cómo lo ejecutarías desde un pipeline de CI/CD.

    **E. Mejora de la aplicación**

    1. Añade un **caché** de las altitudes para no consultar la API de Open-Meteo en cada petición (pista: `functools.lru_cache`).
    2. Añade un endpoint que devuelva los **records por país** y otro que devuelva el **récord más antiguo** y el **más reciente**, y enlázalos desde la interfaz.
    3. Comprueba que los datos de `data/records.json` están al día, y documenta cómo lo verificarías de forma automática.

!!! warning "Atención"
    Documenta adecuadamente con explicaciones y capturas de pantalla los procesos de despliegue de **ambas** aplicaciones Flask, así como las respuestas a las cuestiones planteadas.

    Captura, como mínimo, la salida de `systemctl status` de los dos servicios, la de `curl -i` sobre el virtual host de cada aplicación y la de `journalctl -u <servicio> -n 50`.

---

---

## 17. Referencias

[Documentación de Flask](https://flask.palletsprojects.com/)

[World Athletics - Records](https://worldathletics.org/records)

[API de elevación de Open-Meteo](https://open-meteo.com/en/docs/elevation-api)

[Documentación de Leaflet](https://leafletjs.com/)

[Documentación de Gunicorn](https://docs.gunicorn.org/)

[Guía de despliegue de Flask con Gunicorn y Nginx](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/)

[Guía de despliegue de Flask en producción](https://flask.palletsprojects.com/en/stable/deploying/)

[WSGI: PEP 3333](https://peps.python.org/pep-3333/)

[ASGI: Wikipedia](https://es.wikipedia.org/wiki/ASGI)

[Documentación de `uv`](https://docs.astral.sh/uv/)

[Migración de `pip` a `uv`](https://docs.astral.sh/uv/guides/migration/pip-to-project/)

[`systemd.service`: directivas de hardening](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)

[Deploy Flask The Easy Way With Gunicorn and Nginx!](https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc)

[Deploy flask app with Nginx using Gunicorn](https://faun.pub/deploy-flask-app-with-nginx-using-gunicorn-7fda4f50066a)
