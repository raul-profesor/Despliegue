# Pràctica 2.1 – Instalación y configuración de servidor web Nginx


## Instalación servidor web Nginx

Para instalar el servidor nginx en nuestra Debian, primero actualizamos los repositorios y después instalamos el paquete correspondiente: 

```sh
sudo apt update

sudo apt install nginx
```

Comprobamos que nginx se ha instalado y que está funcionando correctamente: 

```sh
systemctl status nginx

```

!!!info Info
    **Esta práctica se ha hecho con Nginx 1.18.0**

## Creación de las carpeta del sitio web 

Igual que ocurre en Apache, todos los archivos que formarán parte de un sitio web que servirá nginx se organizarán en carpetas. Estas carpetas, típicamente están dentro de `/var/www`. 

Así pues, vamos a crear la carpeta de nuestro sitio web o dominio: 

```sh
sudo mkdir -p /var/www/nombre_web/html
```
Donde el nombre de dominio puede ser la palabra que queráis, sin espacios. 

Ahí, dentro de esa carpeta html, debéis clonar el siguiente repositorio:

`https://github.com/cloudacademy/static-website-example`

Además, haremos que el propietario de esta carpeta y todo lo que haya dentro sea el usuario `www-data`, típicamente el usuario del servicio web.

```sh
sudo chown -R www-data:www-data /var/www/nombre_web/html
```

Y le daremos los permisos adecuados para que no nos de un error de acceso no autorizado al entrar en el sitio web: 

```sh
sudo chmod -R 755 /var/www/nombre_web
```
Para comprobar que el servidor está funcionando y sirviendo páginas correctamente, podéis acceder desde vuestro cliente a: 

```sh
http://IP-maq-virtual
```
Y os deberá aparecer algo así: 

![](img/4.1-1.png)

Lo que demuestra que todo es correcto hasta ahora. 

## Configuración de servidor web NGINX 

En Nginx hay dos rutas importantes. La primera de ellas es **`sites-available`**, que contiene los archivos de configuración de los hosts virtuales o bloques disponibles en el servidor. Es decir, cada uno de los sitios webs que alberga el servido. La otra es **`sites-enabled`**, que contiene los archivos de configuración de los sitios habilitados, es decir, los que funcionan en ese momento. 

Dentro de `sites-available` hay un archivo de configuración por defecto (default), que es la página que se muestra si accedemos al servidor sin indicar ningún sitio web o cuando el sitio web no es encontrado en el servidor (debido a una mala configuración por ejemplo). Esta es la página que nos ha aparecido en el apartado anterior. 

Para que Nginx presente el contenido de nuestra web, es necesario crear un bloque de servidor con las directivas correctas. En vez de modificar el archivo de configuración predeterminado directamente, crearemos uno nuevo en `/etc/nginx/sites-available/nombre_web`: 

```console
sudo nano /etc/nginx/sites-available/vuestro_dominio 
```

Y el contenido de ese archivo de configuración: 

```aconf
server {
        listen 80;
        listen [::]:80;
        root /ruta/absoluta/archivo/index;
        index index.html index.htm index.nginx-debian.html;
        server_name nombre_web;
        location / {
                try_files $uri $uri/ =404;
        }
}
```

Aquí la directiva root debe ir seguida de la ruta absoluta absoluta dónde se encuentre el archivo index.html de nuestra página web, que se encuentra entre todos los que habéis descomprimido. 

Aquí tenéis un ejemplo de un sitio webs con su ruta (directorios que hay) antes del archivo index.html: 

![](img/4.1-2.png)
!!!info
    Ruta → /var/www/ejemplo2/html/2016_soft_landing

Y crearemos un archivo simbólico entre este archivo y el de sitios que están habilitados, para que se dé de alta automáticamente. 

```console
sudo ln -s /etc/nginx/sites-available/nombre_web /etc/nginx/sites-enabled/
```

Y reiniciamos el servidor para aplicar la configuración: 

```sh
sudo systemctl restart nginx
```

## Comprobaciones

### Comprobación del correcto funcionamiento

Como aún no poseemos un servidor DNS que traduzca los nombres a IPs, debemos hacerlo de forma manual. Vamos a editar el archivo `/etc/hosts` <u>**de nuestra máquina anfitriona**</u> para que asocie la IP de la máquina virtual, a nuestro `server_name`.

Este archivo, en Linux, está en: `/etc/hosts`

Y en Windows: ` C:\Windows\System32\drivers\etc\hosts`

Y deberemos añadirle la línea:

 `192.168.X.X nombre_web`
    
donde debéis sustituir la IP por la que tenga vuestra máquina virtual.

!!!warning "¡Atención!"
    Cada vez que iniciamos el laboratorio de AWS, las IPs públicas cambiarán. Tenedlo en cuenta por si tenéis que cambiar esta IP en el archivo hosts al retomar la realización de la práctica.



### Comprobar registros del servidor

Comprobad que las peticiones se están registrando correctamente en los archivos de logs, tanto las correctas como las erróneas: 

+ ```/var/log/nginx/access.log```: cada solicitud a su servidor web se registra en este archivo de registro, a menos que Nginx esté configurado para hacer algo diferente. 
  
+ ```/var/log/nginx/error.log```: cualquier error de Nginx se asentará en este registro.
 
!!!info 
    Si no os aparece nada en los logs, podría pasar que el navegador ha cacheado la página web y que, por tanto, ya no está obteniendo la página del navegador sino de la propia memoria.
    Para solucionar esto, podéis acceder con el *modo privado* del navegador y ya os debería registrar esa actividad en los logs.

## FTP

Si queremos tener varios dominios o sitios web en el mismo servidor nginx (es decir, que tendrán la misma IP) debemos repetir todo el proceso anterior con el nuevo nombre de dominio que queramos configurar.

### ¿Cómo transferir archivos desde nuestra máquina local/anfitrión a nuestra máquina virtual Debian/servidor remoto?

A día de hoy el proceso más sencillo y seguro es a través de Github como hemos visto antes. No obstante, el currículum de la Consellería d'Educació me obliga a enseñaros un método un tanto obsoleto a día de hoy, así que vamos a ello, os presento al FTP.

[El FTP](https://es.wikipedia.org/wiki/Protocolo_de_transferencia_de_archivos) es un protocolo de transferencia de archivos entre sistemas conectados a una red TCP. Como su nombre indica, se trata de un protocolo que permite transferir archivos directamente de un dispositivo a otro. Actualmente, es un protocolo que poco a poco va abandonándose, pero ha estado vigente más de 50 años.

El protocolo FTP tal cual es un protocolo inseguro, ya que su información no viaja cifrada. Sin embargo, en 2001 esto se solucionó con el protocolo **SFTP**, que le añade una capa SSH para hacerlo más seguro y privado.

**SFTP** no es más que el mismo protocolo FTP pero implementado por un canal seguro. Son las siglas de SSH File Transfer Protocol y consiste en una extensión de Secure Shell Protocol (SSH) creada para poder hacer transmisiones de archivos.

La seguridad que nos aporta **SFTP** es importante para la transferencia de archivos porque, si no disponemos de ella, los archivos viajarán tal cual por la red, sin ningún tipo de encriptación. Así pues, usando FTP tradicional, si algún agente consigue escuchar las transferencias, podría ocurrir que la información quedase al descubierto. Esto sería especialmente importante si los archivos que subimos contienen información confidencial o datos personales.

Dado que usar **SFTP** aporta mayor seguridad a las transmisiones, es recomendable utilizarlo, más aún sabiendo que realmente no hay mucha dificultad en establecer las conexiones por el protocolo seguro.

### Configurar servidor SFTP en instancia EC2 (Debian)

Por lo explicado en el apartado anterior, no necesitamos un software que haga de servidor FTP para nuestro objetivo, sino únicamente un servidor de SSH. Precisamente ya tenemos uno instalado en nuestra instancia EC2 (OpenSSH), que es el que venimos usando hasta ahora.

**Sí necesitaremos un cliente de FTP para realizar la conexión, como por ejemplo [Filezilla](https://filezilla-project.org/)**

!!!task "Tarea"
    Configura un nuevo dominio (nombre web) para el .zip con el nuevo sitio web que os proporcionado. **En este caso debéis transferir los archivos a vuestra Debian mediante SFTP.**


Tras descargar <U>**el cliente FTP**</u> en nuestro ordenador, introducimos los datos necesarios para conectarnos a nuestro servidor FTP en Debian:

![](img/sftp1.png)

+ La IP pública de nuestra instancia EC2 Debian (recuadro verde). Debe ir precedida de `sftp://` o en caso contrario habría que indicar que el puerto es el 22.
+ El nombre de usuario de Debian (recuadro rojo)

Tras darle al botón de *Conexión rápida*, se nos muestra un error:

![](img/sftp2.png)

Nos está avisando de algo que ya sabemos. Para conectarnos a esta máquina mediante SSH (puerto 22), o lo que es lo mismo, SFTP, sólo podemos hacerlo mediante el uso de claves. Así pues, necesitamos decirle a *Filezilla* qué clave debe usar. Tan fácil como ir a `Edición > Opciones`y explicitarlo:

![](img/sftp3.png)

Tras ello, la conexión será exitosa y accederemos directamente a la carpeta `home` de nuestro usuario `admin`-

![](img/sftp4.png)


Una vez conectados, buscamos la carpeta de nuestro ordenador donde hemos descargado el *.zip* (en la parte izquierda de la pantalla) y en la parte derecha de la pantalla, buscamos la carpeta donde queremos subirla. Con un doble click o utilizando *botón derecho > subir*, la subimos al servidor.

Recordemos que debemos tener nuestro sitio web en la carpeta `/var/www` y darle los permisos adecuados, de forma similiar a cómo hemos hecho con el otro sitio web. 

El comando que nos permite descomprimir un *.zip* en un directorio concreto es:

```sh
unzip archivo.zip -d /nombre/directorio
```

Si no tuvieráis unzip instalado, lo instaláis:

```sh
sudo apt-get update && sudo apt-get install unzip
```

## HTTPS

En este apartado le añadiremos a nuestro servidor una capa de seguridad necesaria. Haremos que todos nuestros sitios web alojados hagan uso de certificados SSL y se acceda a ellos por medio de HTTPS.

Para ello, a modo de prueba de concepto, nos generaremos unos certificados autofirmados y, en el fichero de configuración de nuestros hosts virtuales (los sitios web que hemos configurado), deberemos cambiar los parámetros necesarios.

Apoyaos en una búsqueda en Internet para conseguir vuestro objetivo.

### Redirección HTTP a HTTPS

Cuando hayáis cumplido con la tarea de dotar de HTTPS a vuestros sitios web, podréis pasar a esta. 

Fijáos que con el estado de la configuración actual, a vuestro sitio web se puede acceder aún de dos formas simultáneas, por el puerto 80 (HTTP e inseguro) y por el puerto 443 (HTTPS, seguro). Puesto que queremos dejar la configuración bien hecha y sin posibles fisuras, vuestro objetivo es que si el usuario accede a vuestro sitio web mediante el puerto 80 (HTTP) automáticamente, por motivos de seguridad, se le redirija a HTTPS, en el puerto 443.

Realizad la búsqueda de información adecuada para conseguir esta redirección automática mediante los cambios necesarios en vuestros archivos de hosts virtuales.


## Cuestiones finales

!!!Task "Cuestión 1"
    ¿Qué pasa si no hago el link simbólico entre ```sites-available``` y ```sites-enabled``` de mi sitio web?

!!!Task "Cuestión 2"
    ¿Qué pasa si no le doy los permisos adecuados a ```/var/www/nombre_web```? 


