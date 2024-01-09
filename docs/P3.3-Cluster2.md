---
title: '(ACTUALIZADA) Práctica 3.3 - Despliegue de una aplicación "clusterizada" con Node Express'
---

# Práctica 3.3: Despliegue de una aplicación "clusterizada" con Node Express

## Introducción

Cuando se construye una aplicación de producción, normalmente se busca la forma de optimizar su rendimiento llegando a una solución de compromiso. En esta práctica echaremos un vistazo a un enfoque que puede ofrecer una victoria rápida cuando se trata de mejorar la manera en que las aplicaciones Node.js manejan la carga de trabajo.

Una instancia de Node.js se ejecuta en un solo hilo, lo que significa que en un sistema multinúcleo (como la mayoría de los ordenadores de hoy en día), no todos los núcleos serán utilizados por la aplicación. Para aprovechar los otros núcleos disponibles, podemos lanzar un cluster de procesos Node.js y distribuir la carga entre ellos.

![](img/imagen_cluster.png)

Tener varios hilos para manejar las peticiones mejora el rendimiento (peticiones/segundo) del servidor, ya que varios clientes pueden ser atendidos simultáneamente. Veremos cómo crear procesos hijos con el módulo de cluster de Node.js para, más tarde, ver cómo gestionar el cluster con el gestor de procesos PM2.

### Un vistazo rápido a los clusters

[El módulo de clúster de Node.js](https://nodejs.org/api/cluster.html) permite la creación de procesos secundarios (*workers*) que se ejecutan simultáneamente y comparten el mismo puerto de servidor. Cada hijo generado tiene su propio ciclo de eventos y memoria. Los procesos secundarios utilizan IPC (comunicación entre procesos) para comunicarse con el proceso principal de Node.js.

Tener múltiples procesos para manejar las solicitudes entrantes significa que se pueden procesar varias solicitudes simultáneamente y si hay una operación de bloqueo/ejecución prolongada en un *worker*, los otros *workers* pueden continuar administrando otras solicitudes entrantes; la aplicación no se detendrá hasta que finalice la operación de bloqueo.

La ejecución de varios *workers* también permite actualizar la aplicación en producción con poco o ningún tiempo de inactividad. Se pueden realizar cambios en la aplicación y reiniciar los *workers* uno por uno, esperando que un proceso secundario se genere por completo antes de reiniciar otro. De esta manera, siempre habrá *workers* ejecutándose mientras se produce la actualización.

Las conexiones entrantes se distribuyen entre los procesos secundarios de dos maneras:

* El proceso maestro escucha las conexiones en un puerto y las distribuye entre los *workers* de forma rotatoria. Este es el enfoque por defecto en todas las plataformas, excepto Windows.

* El proceso maestro crea un socket de escucha y lo envía a los *workers* interesados ​​que luego podrán aceptar conexiones entrantes directamente.

### Usando los clusters

#### Primero sin clúster

Para ver las ventajas que ofrece la agrupación en clústeres, comenzaremos con una aplicación de prueba en Node.js que no usa clústeres y la compararemos con una que sí los usa, se trata de la siguiente.

Primero nos crearemos un directorio para los archivos que utilizaremos: `mkdir ....` y con `cd` nos ubicaremos dentro de dicho directorio.

Trase ello, inicializamos el proyecto, lo que creará un **package.json** automáticamente:

```console
npm init -y
```  
!!!note "Nota"
    Cuando lo acompañamos con `-y`, le estamos diciendo a NPM que acepte todas las opciones por defecto.

Al **package.json** generado hemos de añadirle las siguiente línea:

```json
  "type": "module"
```
Tal y como podéis ver en la imagen (cuidado con la *coma*):

![](img/%20cluster-nuevo1.png)

Y tras esto, instalaremos las herramientas que nos harán falta en el resto de la práctica, si es que no las teníamos ya:

```sh
npm install express
```
Y de forma global:

```sh
npm install -g loadtest pm2
```

Y ahora creemos una aplicación sencilla que ejecutará una tarea intensiva de CPU cada vez que la ejecute el usuario. Este pequeño programa aún no utilizará el módulo `cluster` para que de esta manera sólo se ejecute una sola instancia en la CPU cada vez que se lance. Más tarde la compararemos con otra utilizando dicho módulo.

Cread en el directorio el siguiente archivo:

```javascript title="index.js"
//Se importa el paquete "express", se establece el p uerto a 3000 y se crea la variable app como una instancia de express
import express from "express";

const port = 3000;
const app = express();

console.log(`worker pid=${process.pid}`);

//se crea el bucle que ejecutará la carga intensiva puesto que incrementa la variable "total", 5 millones de veces

app.get("/carga", (req, res) => {
          let total = 0;
          for (let i = 0; i < 5_000_000; i++) {
                      total++;
                    }
          res.send(`El resultado de la tarea instensiva de la CPU es ${total}\n`);
});

//Ponemos a escuchar nuestra aplicación en el puerto anteriormente definido
app.listen(port, () => {
          console.log(`Aplicación escuchando en puerto ${port}`);
});
```

Se trata de una aplicación un tanto *prefabricada* en el sentido de que es algo que jamás encontraríamos en el mundo real. No obstante, nos servirá para ilustrar nuestro propósito.


!!!task "Resumen"
    1. Debéis conectaros al servidor Debian mediante SSH
    2. Debéis crear un directorio para el proyecto de esta aplicación
    3. DENTRO del directorio debéis iniciar el proyecto y modificar el *package.json*
    4. Tras esto, DENTRO del directorio, ya podéis iniciar la aplicación con: `node index.js`

Se debe mostrar el **id** del proceso corriendo y un mensaje confirmando que el servidor está escuchando en el puerto 3000.

Para comprobarlo, podéis acceder a `http://IP-maq-virtual:3000`, done `IP-maq-virtual` es la IP de vuestra Debian. Podéis hacerlo de dos formas:

1. Utilizando `curl` desde cualquier terminal de otra máquina:
    
    `curl http://IP-maq-virtual:3000/carga`
    
2. Desde un navegador web desde cualquier otra máquina.

La salida debe ofrecernos el resultado del cálculo intensivo.

Cuando ejecutamos el archivo `index.js`` con el comando node, el sistema operativo crea un proceso. Un proceso es una abstracción que el sistema operativo hace para un programa en ejecución. El SO asigna memoria para el programa y crea una entrada en una lista que contiene todos los procesos del SO. Esa entrada es un ID de proceso.

El binario del programa se localiza y se carga en la memoria asignada al proceso. A partir de ahí, comienza a ejecutarse. Mientras se ejecuta, no tiene conocimiento de otros procesos en el sistema, y cualquier cosa que ocurra en el proceso no afecta a otros procesos.

#### ¡Ahora con más clúster!

Ahora usaremos el módulo de clúster en la aplicación para generar algunos procesos secundarios y ver cómo eso mejora las cosas.

Crearemos un nuevo archivo llamado `primary.js`que será la aplicación anterior utilizando el módulo cluster. A continuación se muestra el archivo que contiene la lógica de los cluster:

```javascript title="primary.js"
//importamos módulos cluster y os y además todo lo necesario para conocer la ubicación del "index.js"
import cluster from "cluster";
import os from "os";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

//Parte de código que hace referencia a "index.js"
//Se determina el número de CPUs de la máquina y se loguean el PID del proceso principal, que es el que recibirá 
//todas las peticiones y las distribuirá a los workers
const cpuCount = os.cpus().length;

console.log(`El número total de CPUs es ${cpuCount}`);
console.log(`Primario pid=${process.pid}`);
cluster.setupPrimary({
          exec: __dirname + "/index.js",
});

//Este bucle itera tantas veces como núcleos hay en la máquina, llamando al método fork para crear el worker
for (let i = 0; i < cpuCount; i++) {
          cluster.fork();
}
cluster.on("exit", (worker, code, signal) => {
          console.log(`El worker ${worker.process.pid} ha sido aniquilado`);
          console.log("Iniciando otro worker");
          cluster.fork();
});
```

Creamos tantos procesos secundarios como núcleos de CPU hay en la máquina en la que se ejecuta la aplicación. Se recomienda no crear más *workers* que núcleos lógicos en la computadora, ya que esto puede causar una sobrecarga en términos de costos de programación. Esto sucede porque el sistema tendrá que programar todos los procesos creados para que se vayan ejecutando por turnos en los núcleos.

Los *workers* son creados y administrados por el proceso maestro. 

Si el proceso es un maestro, llamamos a `cluster.fork()` para generar varios procesos. Registramos los ID de proceso maestro y *worker*. Cuando un proceso secundario muere, generamos uno nuevo para seguir utilizando los núcleos de CPU disponibles.

Si ejecutamos ahora **primary.js** con `node primary.js`, veremos que se indica que se crea un proceso primario y tantos secundarios como núcleos tenga la máquina, escuchando en el puerto 3000.

Comprueba también que todo funciona correctamente con `curl` o  con un navegador web, igual que antes.

!!!note
    Con varios *workers* disponibles para aceptar solicitudes, se mejoran tanto la disponibilidad del servidor como el rendimiento.


#### Métricas de rendimiento

Realizaremos una prueba de carga en nuestras aplicación para ver cómo maneja una gran cantidad de conexiones entrantes. Usaremos el paquete `loadtest` instalado al inicio para esto.

El paquete `loadtest` nos permite simular una gran cantidad de conexiones simultáneas a nuestra aplicación para que podamos medir su rendimiento.

Primeramente, iniciamos nuestra aplicación sin cluster:

`node index.js``

Y cuando ya tengamos la aplicación corriendo y a la escucha, ejecutamos a la vez **loadtest** para las métricas:

```bash
loadtest -n 1200 -c 200 -k http://localhost:3000/
```

La opción `-n` indica el número de peticiones o solicitudes que se envían a la aplicación, mientras que la opción `-c` indica cuántas de esas peticiones serán concurrentes (simultáneas).

La salida de esta prueba con ***loadtest*** nos ofrecerá múltiples métricas:

+ Total time: cuánto tiempo han tardado en procesarse todas las peticiones.
+ Requests per second (rps): número de peticiones que el servidor puede manejar por segundo
+ Mean latency: mide el tiempo medio que tarda una petición en ser enviada y obtener una respuesta

!!!warning "Atención"
    Estas métricas variarán en función de la máquina y sus características.

!!!task "Tarea"
    Realiza y documenta adecuadamente esta prueba, en primera instancia con la aplicación sin clusters `index.js` y, posteriormente, con clusters (`primary.js`).
    Compara y comenta los resultados.

#### Uso de PM2 para administrar un clúster de Node.js

En nuestra aplicación, hemos usado el módulo `cluster` de Node.js para crear y administrar manualmente los procesos.

Primero hemos determinado la cantidad de *workers* (usando la cantidad de núcleos de CPU como referencia), luego los hemos generado y, finalmente, escuchamos si hay *workers* muertos para poder generar nuevos.

En nuestra aplicación de ejemplo muy sencilla, tuvimos que escribir una cantidad considerable de código solo para administración la agrupación en clústeres. En una aplicación de producción es bastante probable que se deba escribir aún más código.

Existe una herramienta que nos puede ayudar a administrar todo esto un poco mejor: el administrador de procesos `PM2` que hemos instalado al principio. `PM2` es un administrador de procesos de producción para aplicaciones Node.js con un balanceador de carga incorporado.

Cuando está configurado correctamente, `PM2` ejecuta automáticamente la aplicación en modo de clúster, generando *workers* y se encarga de generar nuevos *workers* cuando uno de ellos muera.

`PM2` facilita la parada, eliminación e inicio de procesos, además de disponer de algunas herramientas de monitorización que pueden ayudarnos a monitorizar y ajustar el rendimiento de su aplicación.

Vamos a utilizarlo con nuestra primera aplicación, la que no estaba "clusterizada" en el código. Para ello ejecutaremos el siguiente comando:

```sh
pm2 start index.js -i 0
```

Donde:

+ `-i` <número workers> le indicará a `PM2` que inicie la aplicación en `cluster_mode` (a diferencia de `fork_mode`).

    Si <número workers>se establece a 0, `PM2` generará automáticamente tantos *workers* como núcleos de CPU haya.

Y así, nuestra aplicación se ejecuta en modo de clúster, sin necesidad de cambios de código. 

!!!task
    Ejecuta y documenta con capturas de pantallas, las misma prueba que antes utilizando `loadtest` pero utilizando PM2 y comprueba si se obtienen los mismos resultados. Obviamente, hablamos de la aplicación clusterizada.

Por detrás, `PM2` también utiliza el módulo `cluster` de Node.js, así como otras herramientas que facilitan la gestión de procesos.

En el Terminal, obtendremos una tabla que muestra algunos detalles de los procesos generados.

Podemos detener la aplicación con el siguiente comando:

```sh
pm2 stop app.js
```

La aplicación se desconectará y la salida por terminal mostrará todos los procesos con un estado `stopped`.

En vez de tener pasar siempre las configuraciones cuando ejecuta la aplicación con `pm2 start app.js -i 0`, podríamos facilitarnos la tarea y guardarlas en un archivo de configuración separado, llamado [Ecosystem](https://pm2.keymetrics.io/docs/usage/application-declaration/). 

Este archivo también nos permite establecer configuraciones específicas para diferentes aplicaciones.

Crearemos el archivo *Ecosystem* con el siguiente comando:

![](img/ecosystem.png)

Que generará un archivo llamado ***ecosystem.config.js***. Para poder utilizar módulos, debéis renombrarlo a ***ecosystem.config.cjs***. Tras ello y para el caso concreto de nuestra aplicación, necesitamos modificarlo como se muestra a continuación:

```yaml
module.exports = {
 apps: [
 {
 name: "nombre_aplicacion", 
  script: "index.js",
 instances: 0,
 exec_mode: "cluster", 
 },
 ],
};
```

Al configurar `exec_mode` con el valor `cluster`, le indica a `PM2` que balancee la carga entre cada instancia. `instances` está configurado a **0** como antes, lo que generará tantos *workers* como núcleos de CPU.

La opción `-i` o `instances` se puede establecer con los siguientes valores:

  + `0` o `max`(en desuso) para "repartir" la aplicación entre todas las CPU

  + `-1` para "repartir" la aplicación en todas las CPU - 1

  + `número` para difundir la aplicación a través de un número concreto de CPU

Ahora podemos ejecutar la aplicación con:

```sh
pm2 start ecosystem.config.cjs
```

La aplicación se ejecutará en modo clúster, exactamente como antes y podremos realizar las pruebas que necesitemos.

!!!task "Tarea"
    Recoge las métricas con `loadtest` y este nuevo método para gestionar clusters. Compara y explica los resultados con los casos anteriores.

Podremos iniciar, reiniciar, recargar, detener y eliminar una aplicación con los siguientes comandos, respectivamente:

```sh
$ pm2 start nombre_aplicacion
$ pm2 restart nombre_aplicacion
$ pm2 reload nombre_aplicacion
$ pm2 stop nombre_aplicacion
$ pm2 delete nombre_aplicacion
 
# Cuando usemos el archivo Ecosystem:
 
$ pm2 [start|restart|reload|stop|delete] ecosystem.config.cjs
```

El comando `restart` elimina y reinicia inmediatamente los procesos, mientras que el comando `reload` logra un tiempo de inactividad de 0 segundos donde los *workers* se reinician uno por uno, esperando que aparezca un nuevo *worker* antes de matar al anterior.

También puede verificar el estado, los registros y las métricas de las aplicaciones en ejecución.

!!!task
    Investiga los siguientes comandos y explica que salida por terminal nos ofrecen y para qué se utilizan:

    ```sh
    pm2 ls
    pm2 logs
    pm2 monit
    ```

    Identifica en los logs la creación de los workers y la aplicación a la escucha en el puerto indicado.


!!!warning
    Documenta la realización de toda esta práctica adecuadamente, con las explicaciones y justificaciones necesarias, las respuestas a las preguntas planteadas y las capturas de pantalla pertinentes.

## Cuestiones

Fijáos en las siguientes imágenes:

![](img/loadtest_no_cluster_3.png)

![](img/loadtest_cluster_3.png)


La primera imagen ilustra los resultados de unas pruebas de carga sobre una aplicación sin clúster y la segunda sobre la aplicación clusterizada.

¿Sabrías decir por qué en algunos casos concretos, como este, la aplicación sin clusterizar tiene mejores resultados?

## Referencias

[How to install ExpressJS on Debian 11?](https://unixcop.com/how-to-install-expressjs-on-debian-11/)

[Improving Node.js Application Performance With Clustering](https://blog.appsignal.com/2021/02/03/improving-node-application-performance-with-clustering.html)

[How To Scale Node.js Applications with Clustering](https://www.digitalocean.com/community/tutorials/how-to-scale-node-js-applications-with-clustering)


## Evaluación

De acuerdo a la rúbrica publicada en Aules.