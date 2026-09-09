# Guía Completa de Amazon Web Services (AWS) para Principiantes

## Tabla de Contenidos

1. [¿Qué es la nube?](#qué-es-la-nube)
2. [¿Qué es AWS?](#qué-es-aws)
3. [AWS Academy: qué es y cómo acceder](#aws-academy-qué-es-y-cómo-acceder)
4. [Conceptos fundamentales de AWS](#conceptos-fundamentales-de-aws)
5. [El panel de AWS: la consola de gestión](#el-panel-de-aws-la-consola-de-gestión)
6. [Regiones y zonas de disponibilidad](#regiones-y-zonas-de-disponibilidad)
7. [Servicios esenciales de AWS](#servicios-esenciales-de-aws)
8. [Amazon EC2: Tu primer servidor en la nube](#amazon-ec2-tu-primer-servidor-en-la-nube)
9. [Tipos de instancias EC2](#tipos-de-instancias-ec2)
10. [Creando tu primera instancia EC2](#creando-tu-primera-instancia-ec2)
11. [Grupos de seguridad: el firewall de AWS](#grupos-de-seguridad-el-firewall-de-aws)
12. [Conectándose a EC2 mediante SSH](#conectándose-a-ec2-mediante-ssh)
13. [Gestión de claves SSH](#gestión-de-claves-ssh)
14. [Almacenamiento: EBS y S3](#almacenamiento-ebs-y-s3)
15. [Redes básicas: VPC simplificado](#redes-básicas-vpc-simplificado)
16. [Costes y economía de AWS](#costes-y-economía-de-aws)
17. [Buenas prácticas de seguridad](#buenas-prácticas-de-seguridad)
18. [Glosario de términos AWS](#glosario-de-términos-aws)

---

## ¿Qué es la nube?

Antes de entender qué es AWS, necesitamos comprender qué significa "la nube" en el contexto de la informática. El término "nube" es una metáfora que se usa ampliamente, pero ¿qué significa realmente?

### La nube como concepto

En términos sencillos, "la nube" se refiere a servidores computers accesibles a través de internet, junto con el software que在这些 servidores上运行, las bases de datos que almacenan datos, y los servicios que potencian aplicaciones. En lugar de poseer y mantener tu propio centro de datos físico y servidores, puedes acceder a recursos de computación bajo demanda desde proveedores como AWS, Azure o Google Cloud.

Históricamente, si una empresa quería ejecutar una aplicación web, necesitaba:

1. **Comprar o alquilar espacio en un datacenter físico**: Un cuarto oscuro con servidores propios, o espacio en un centro de datos de terceros
2. **Adquirir servidores físicos**: Máquinas con CPU, RAM, disco duro, que había que rackear, cablear, configurar
3. **Instalar software de virtualización**: Para aprovechar efficiently los recursos de cada servidor
4. **Configurar redes**: Switches, routers, firewalls, conexiones a internet con ancho de banda dedicado
5. **Contratar técnicos especializados**: Para mantener todo esto funcionando 24/7
6. **Planificar la capacidad**: ¿Cuántos servidores necesito? ¿Y si crezco? ¿Y si tengo picos de tráfico?
7. **Pagar facturas de electricidad**: Servidores que consumen mucha energía y generan mucho calor

Este modelo tradicional se llama "on-premises" o "infraestructura on-premise".

Con la nube, todo eso desaparece. En lugar de poseer servidores, alquilas recursos de computación a un proveedor que:

- Tiene datacenters distribuidos por todo el mundo
- Mantiene y actualiza el hardware por ti
- Escala los recursos hacia arriba o hacia abajo según tus necesidades
- Solo te cobra por lo que usas, cuando lo usas

### Modelos de servicio en la nube

La industria de la nube define tres modelos de servicio principales, que representan diferentes niveles de abstracción:

**Infrastructure as a Service (IaaS)**: El proveedor ofrece acceso a recursos de computación básicos: servidores virtuales, almacenamiento y redes. Tú eres responsable de instalar el sistema operativo, configurar el software y gestionar la infraestructura. AWS EC2 es un ejemplo de IaaS.

**Platform as a Service (PaaS)**: El proveedor gestiona más cosas por ti. Tú simplemente despliegas tu aplicación sin preocuparte por el servidor, el sistema operativo o la infraestructura de red. AWS Elastic Beanstalk o Heroku son ejemplos.

**Software as a Service (SaaS)**: El proveedor ofrece aplicaciones completas funcionando en la nube. Gmail, Spotify o Salesforce son ejemplos de SaaS. No instalas nada, solo usas la aplicación.

Terraform y Ansible, tal como viste en el documento anterior, operan principalmente en la capa IaaS, ayudándote a gestionar esa infraestructura de forma programable.

### Beneficios de la nube

La nube ofrece varias ventajas sobre la infraestructura tradicional:

**Elasticidad**: ¿Necesitas 10 servidores mañana y 100 hoy? Con la nube, puedes escalar hacia arriba y hacia abajo según la demanda, generalmente con unos pocos clics o una llamada a una API.

**Coste**: No hay inversión inicial en hardware. Pagas por uso, como el agua o la electricidad. Además, puedes reducir costes apagando recursos que no necesites (por ejemplo, entornos de desarrollo fuera de horario laboral).

**Velocidad**: En lugar de esperar semanas para que llegue hardware nuevo, puedes tener un servidor virtual funcionando en minutos.

**Alcance global**: Los grandes proveedores tienen datacenters en dozens de ubicaciones por todo el mundo. Puedes desplegar aplicaciones cerca de tus usuarios sin importar dónde estén.

**Fiabilidad**: Los datacenters de los grandes proveedores están diseñados para soportar fallos. Si un servidor se estropea, tu aplicación sigue funcionando porque el proveedor redistribuye la carga. Además, hacen backup de tus datos de forma automática.

### ¿Qué es "on-demand" vs "reserved"?

Dos conceptos importantes en la nube:

**On-Demand (bajo demanda)**: Pagas por hora de uso, sin compromisos a largo plazo. Es como taxis: pagas por el viaje cuando lo necesitas. Conveniente para flexibilidad, pero más caro por hora.

**Reserved (reservado)**: Te comprometes a usar un recurso durante 1-3 años y recibes un descuento significativo (hasta un 70%). Es como comprar un coche en lugar de taxi: inversión inicial, pero más barato a largo plazo.

Para estudiantes aprendiendo, el modelo on-demand es ideal porque puedes experimentar sin grandes compromisos.

---

## ¿Qué es AWS?

Amazon Web Services (AWS) es la subsidiaria de Amazon que proporciona una plataforma de computación en la nube pública. Lanzada oficialmente en 2002 como un conjunto de servicios web internos de Amazon, AWS se convirtió en una subsidiaria separada en 2003 y ha crecido hasta convertirse en el mayor proveedor de servicios de nube del mundo.

AWS ofrece más de 200 servicios diferentes que van desde computación básica hasta inteligencia artificial, machine learning, IoT, y mucho más. Esta enorme variedad puede resultar abrumadora al principio, pero la mayoría de los estudiantes y proyectos начинают con un pequeño subconjunto de servicios fundamentales.

### Los servicios más importantes de AWS

Aunque AWS tiene cientos de servicios, unos pocos son los más fundamentales y los que más vas a usar:

**Amazon EC2 (Elastic Compute Cloud)**: Máquinas virtuales (servidores) en la nube. Es el servicio más básico y el que más vas a usar para aprender. Te permite crear servidores de diferentes tamaños y sistemas operativos en minutos.

**Amazon S3 (Simple Storage Service)**: Almacenamiento de objetos en la nube. Piensa en él como un sistema de archivos enorme en internet donde guardas archivos. Muy usado para alojar archivos estáticos, backups, datos de aplicaciones, etc.

**Amazon RDS (Relational Database Service)**: Bases de datos gestionadas. En lugar de instalar y mantener MySQL, PostgreSQL u Oracle tú mismo, RDS lo hace por ti, manejando backups, actualizaciones y replicación.

**Amazon VPC (Virtual Private Cloud)**: Redes virtuales privadas. Te permite crear redes lógicamente aisladas dentro de la infraestructura de AWS, con control total sobre la topología de red.

**Amazon IAM (Identity and Access Management)**: Gestión de identidades y accesos. Controla quién puede hacer qué dentro de tu cuenta de AWS, definiendo permisos granulares.

**Amazon CloudWatch**: Monitorización y observabilidad. Te permite ver métricas, logs y alarmas de tus servicios AWS.

**AWS Lambda**: Computación sin servidores. Puedes ejecutar código sin aprovisionar ni gestionar servidores, pagando solo por el tiempo de ejecución.

### AWS vs otros proveedores de nube

El mercado de cloud pública está dominado por tres grandes proveedores:

| Proveedor | Cuota de mercado | Particularidades |
|-----------|------------------|------------------|
| **AWS** | ~32% | El más antiguo, el más amplio, el más usado en la industria |
| **Microsoft Azure** | ~23% | Muy fuerte en entorno empresarial y Windows |
| **Google Cloud Platform** | ~10% | Fuerte en datos, machine learning y Kubernetes |

Para aprender, cualquier proveedor es válido. AWS es el más extendido en la industria, lo que significa más documentación, más tutoriales, y más conocimiento disponible en internet.

---

## AWS Academy: qué es y cómo acceder

AWS Academy es un programa educativo de Amazon diseñado para instituciones académicas. Proporciona a estudiantes acceso gratuito a recursos de aprendizaje de AWS, laboratorios prácticos, y lo más importante: créditos gratuitos de AWS para práctica y experimentación.

### ¿Qué incluye AWS Academy?

**Contenido curricular**: Cursos diseñados por AWS, disponibles a través de la plataforma AWS Academy. Cubren desde fundamentos hasta temas avanzados como machine learning, seguridad y arquitectura.

**Laboratorios prácticos**: Entornos donde puedes experimentar con servicios reales de AWS sin temor a romper algo o acumular facturas inesperadas.

**Creditos AWS**: Dependiendo de tu institución y curso, recibes créditos (generalmente entre $100-$300) que puedes usar para crear recursos reales en AWS. Esto te permite experimentar con la consola real y servicios reales.

**Certificaciones**: Descuentos o exámenes gratuitos para obtener certificaciones AWS, que son muy valoradas en la industria.

### Cómo注册 y empezar

El proceso típico depende de tu institución, pero generalmente:

1. **Tu instructor o institución te proporcionará un enlace de invitación** o un código de acceso a AWS Academy. Sin esto, no puedes acceder.

2. **Regístrate en AWS Academy**: Ve a https://awsacademy.com y crea una cuenta con tu email institucional o el que te proporcionen.

3. **Accede al Learning Management System (LMS)**: Una vez registrado, tendrás acceso a los cursos. Aquí encontrarás:
   - Fundamentos de arquitecturas en la nube
   - Laboratorios prácticos guiados paso a paso
   - Exámenes de práctica

4. **Activa tus créditos AWS**:
   - Entra en la consola de AWS con las credenciales de AWS Academy (no tu cuenta personal de AWS)
   - Los créditos se aplican automáticamente a tu cuenta
   - IMPORTANTE: Usa solo esta cuenta para prácticas, no mezcles con otras cuentas

### Diferencia entre AWS Academy y cuenta AWS normal

| Aspecto | AWS Academy | Cuenta AWS normal |
|---------|-------------|-------------------|
| **Coste** | Créditos educativos gratuitos | Pagas por uso real |
| **Acceso** | Cuenta proporcionada por la institución | Creada por ti |
| **Límites** | Servicios limitados generalmente | Límites estándar de AWS |
| **Propósito** | Aprendizaje | Producción o desarrollo personal |
| **Soporte** | A través del LMS de Academy | Documentación pública o soporte de pago |

### Primeros pasos en la consola de AWS Academy

Una vez dentro de tu cuenta de AWS Academy:

1. **Accede a la consola de gestión**: https://console.aws.amazon.com

2. **Explora el menú de servicios**: En la esquina superior izquierda, verás un menú desplegable con todos los servicios AWS. Al principio, quédate solo con los fundamentales.

3. **Selecciona tu región**: En la esquina superior derecha, hay un selector de región. Para comenzar, usa una región cercana a tu ubicación como `US East (N. Virginia)` o `EU (Ireland)`.

4. **Crea recursos poco a poco**: No intentes crear todo de golpe. Empieza con una simple instancia EC2, aprende cómo funciona, y ve avanzando.

### Consejos para estudiantes de AWS Academy

**No tengas miedo de explorar**: La cuenta de AWS Academy está pensada para que experimentes. Los recursos que crees típicamente tienen límites razonables.

**Lee las advertencias de coste**: AWS te avisa cuando estás a punto de crear recursos que pueden ser costosos. Presta atención a estos avisos.

**Destruye lo que no uses**: Si creas recursos para una práctica y luego no los necesitas, elimínalos. Así ahorras créditos para futuras prácticas.

**Anota lo que aprendes**: Lleva un cuaderno o documento donde registres qué hiciste, qué funcionó y qué no. Te servirá como referencia futura.

---

## Conceptos fundamentales de AWS

Antes de empezar a crear recursos, hay algunos conceptos fundamentales que necesitas entender sobre cómo funciona AWS.

### Todo es una API

AWS funciona mediante APIs (Application Programming Interfaces). Cada acción que realizas en la consola web, ya sea crear una instancia o subir un archivo, se convierte internamente en llamadas a la API de AWS.

Esto significa que:

- **La consola web es solo una interfaz**: Hace las mismas llamadas API que podrías hacer tú programáticamente
- **Puedes automatizar todo**: Con herramientas como Terraform o el AWS CLI, puedes hacer cualquier cosa que hagas en la consola
- **Todo tiene límites y cuotas**: Las APIs tienen rate limits, lo que significa que hay un número máximo de llamadas por segundo

### Everything is regional... except...

La mayoría de los servicios en AWS son regionales, lo que significa que eliges una región geográfica específica y tus recursos se crean en esa ubicación física. Sin embargo, hay excepciones importantes:

**Servicios globales**: IAM, Route 53 (DNS), CloudFront (CDN) no están atados a una región específica.

**Servicios de infraestructura global**: Los servicios de red como VPC requieren decisiones específicas de región, pero las arquitecturas pueden diseñarse para cubrir múltiples regiones.

### Recursos y sus identificadores

Cada recurso en AWS tiene un identificador único. Los más comunes son:

**ARN (Amazon Resource Name)**: El identificador único universal para cualquier recurso AWS. Tiene un formato específico:

```
arn:aws:service:region:account-id:resource-type/resource-id
arn:aws:ec2:us-east-1:123456789012:instance/i-0abc123def456789
```

**Resource IDs**: Identificadores específicos por tipo de recurso. Por ejemplo:
- Instancias EC2: `i-0abc123def456789`
- Buckets S3: `mi-bucket-unico` (debe ser globalmente único)
- Bases de datos RDS: `db-ABCDEFGHIJKLMNOP`

### El concepto de "resource"

En AWS, casi todo lo que creas es un "recurso". Una instancia EC2 es un recurso. Un bucket S3 es un recurso. Un usuario IAM es un recurso. Esta terminología es importante porque IAM (gestión de identidades y accesos) te permite dar permisos específicos a nivel de recurso.

---

## El panel de AWS: la consola de gestión

La Consola de Gestión de AWS es la interfaz web que te permite interactuar con todos los servicios de AWS. Aunque puede parecer abrumadora al principio, tiene una estructura relativamente sencilla una vez que la entiendes.

### Navegación básica

**Barra de navegación superior**:
- **Logo de AWS**: Te lleva al dashboard principal
- **Selector de región**: Elige la región donde trabajarás. Recuerda: la mayoría de los recursos son regionales.
- **Cuadro de búsqueda de servicios**: Si sabes lo que buscas, escribe aquí (ej: "EC2", "S3")
- **Notificaciones**: Alertas y anuncios
- **Cuenta y soporte**: Información de tu cuenta, cambiar región, cerrar sesión

**Menú de servicios (esquina superior izquierda)**:
- Click en "Servicios" para ver el menú completo
- Los servicios están categorizados: Compute, Storage, Database, Networking, etc.
- Tu最近 utilizado muestra los servicios que has usado recientemente
- Los "favoritos" te permiten guardar servicios que uses mucho (estrellita)

### El dashboard

Cuando entras en la consola sin un servicio seleccionado, ves el Dashboard. Aquí encontrarás:

- **Resumen de servicios populares**: Enlaces directos a los servicios más usados
- **Panel de facturación**: Uso de créditos, costes acumulados
- **Recursos recientes**: Recursos que has creado o modificado recientemente
- **Noticias y announcements**: Información de AWS

### Buscador de servicios

Si sabes qué servicio quieres usar, escribe su nombre en el buscador de la esquina superior. Por ejemplo, escribe "EC2" y verás sugerencias:

- EC2
- EC2 Image Builder
- EC2 Instance Connect
- ...

Click en el primero y te lleva directamente al panel de ese servicio.

### Panel de un servicio específico

Cada servicio tiene su propio panel con:

- **Navegación izquierda**: Categorías dentro del servicio (ej: en EC2: Instances, Images, Key Pairs, Security Groups, etc.)
- **Área principal**: Lista de recursos, detalles, acciones
- **Barra de acciones**: Botones como "Launch Instance", "Create", "Delete"

---

## Regiones y zonas de disponibilidad

Entender regiones y zonas de disponibilidad es fundamental para trabajar effectively con AWS.

### Regiones

Una región es una ubicación geográfica que contiene múltiples zonas de disponibilidad. AWS tiene regiones en todo el mundo:

| Región | Nombre | Ubicación |
|--------|--------|-----------|
| us-east-1 | US East (N. Virginia) | Estados Unidos |
| us-west-2 | US West (Oregon) | Estados Unidos |
| eu-west-1 | EU (Ireland) | Europa |
| eu-central-1 | EU (Frankfurt) | Europa |
| ap-southeast-1 | Asia Pacific (Singapore) | Asia |
| ap-northeast-1 | Asia Pacific (Tokyo) | Asia |

**¿Por qué importa la región?**

- **Latencia**: Elige una región cerca de tus usuarios para menor latencia
- **Coste**: Los precios varían por región
- **Servicios disponibles**: Algunos servicios no están en todas las regiones
- **Compliance**: Algunas regulaciones requieren que los datos se guarden en regiones específicas

Para aprender, usa cualquier región principal. `us-east-1` o `eu-west-1` son buenas opciones porque tienen todos los servicios disponibles.

### Zonas de disponibilidad (AZs)

Cada región contiene múltiples zonas de disponibilidad, típicamente 3-6. Una zona de disponibilidad es un centro de datos completo con sus propios:

- Fuentes de energía independientes
- Sistemas de refrigeración
- Redes de conectividad

Pero que está ubicado relativamente cerca de las otras AZs de la región (dentro de unos pocos kilómetros). Esto permite:

- **Alta disponibilidad**: Si una AZ falla, las otras siguen funcionando
- **Baja latencia entre AZs**: La comunicación entre AZs es rápida
- **Replica synchrone**: Para bases de datos y aplicaciones que necesitan redundancia

Cuando creas recursos críticos, puedes distribuirlos across múltiples AZs para mayor redundancia.

### Selección de región

Para la mayoría de las prácticas de este curso:

1. Abre la consola de AWS
2. Mira la esquina superior derecha
3. Click en el selector de región
4. Selecciona `US East (N. Virginia)` o `EU (Ireland)` o la que prefieras
5. Los recursos que crees estarán en esa región

**Importante**: Si cambias de región, los recursos que creaste en otra región no aparecerán. Cada región es independiente.

---

## Servicios esenciales de AWS

Vamos a revisar brevemente los servicios que más vas a usar, aunque profundizaremos en algunos más adelante.

### Amazon EC2: Computación en la nube

EC2 es el servicio más fundamental de AWS. Te permite crear máquinas virtuales (instancias) con diferentes sistemas operativos (Linux, Windows) y especificaciones (CPU, RAM, almacenamiento).

Cada instancia EC2 es esencialmente un servidor en la nube que puedes:

- Elegir su sistema operativo (Amazon Linux, Ubuntu, Windows Server, etc.)
- Seleccionar su tamaño (CPU y RAM)
- Configurar su almacenamiento
- Conectarte por SSH (Linux) o RDP (Windows)
- Instalar cualquier software que necesites

### Amazon S3: Almacenamiento simple

S3 es un servicio de almacenamiento de objetos. Piensa en él como un sistema de archivos infinito en internet.

Características principales:

- **Buckets**: Los contenedores donde guardas archivos. Cada bucket tiene un nombre único globalmente.
- **Objetos**: Los archivos que guardas. Cada objeto tiene una clave (path) y metadatos.
- **Durabilidad**: 99.999999999% (once nueves) de durabilidad. Tus datos están muy seguros.
- **Coste**: Pagas por GB almacenado y porRequests de lectura/escritura.

Usos comunes:

- Alojar archivos estáticos de aplicaciones web (HTML, CSS, JS, imágenes)
- Backup de datos
- Data Lakes para análisis
- Distribución de contenido con CloudFront

### Amazon VPC: Redes privadas virtuales

VPC te permite crear redes virtuales privadas en AWS. Es como crear tu propia red de area local pero en la nube.

Con VPC puedes:

- Definir rangos de direcciones IP privadas (ej: 10.0.0.0/16)
- Crear subredes públicas y privadas
- Configurar routers y tablas de enrutamiento
- Implementar firewalls (Security Groups, Network ACLs)
- Conectar a otras redes (VPN, Direct Connect)

Cuando creas recursos como instancias EC2, necesitas especificar en qué VPC y subred se crean.

### Amazon IAM: Gestión de identidades

IAM te permite controlar quién puede acceder a qué recursos de AWS. Es fundamental para la seguridad.

Conceptos principales:

- **Usuarios**: Cuentas individuales para personas
- **Grupos**: Colecciones de usuarios con permisos comunes
- **Roles**: Permisos que puedes asignar a recursos o usuarios temporales
- **Políticas**: Documentos JSON que definen permisos específicos

Por defecto, todo está denegado. Solo puedes acceder a lo que explícitamente se permite.

### Amazon RDS: Bases de datos gestionadas

RDS te proporciona bases de datos relacionales gestionadas sin tener que instalar y mantener el motor de base de datos tú mismo.

Motores disponibles:

- MySQL
- PostgreSQL
- MariaDB
- Oracle
- SQL Server

RDS maneja por ti:

- Backups automáticos
- Parches de software
- Replicación para alta disponibilidad
- Failover automático si una AZ deja de funcionar

### Amazon CloudWatch: Monitorización

CloudWatch recopila métricas y logs de tus recursos AWS y aplicaciones.

Puedes ver:

- Uso de CPU de tus instancias EC2
- Tráfico de red
- Logs de aplicaciones
- Crear alarmas que te alertan cuando algo supera un umbral

### AWS Lambda: Computación sin servidor

Lambda te permite ejecutar código sin aprovisionar servidores. Solo escribes el código, lo subes, y Lambda lo ejecuta en respuesta a eventos.

Pagas por cada 100ms de ejecución y por número de invocaciones, no por hora de servidor.

---

## Amazon EC2: Tu primer servidor en la nube

Amazon EC2 (Elastic Compute Cloud) es el servicio más importante de AWS para aprender. Una instancia EC2 es simplemente un servidor virtual con las características que tú elijas.

### ¿Qué es una instancia EC2?

Una instancia EC2 es una máquina virtual en la nube de AWS. Es como tener un ordenador accesible desde internet en el que tú decides:

- **Sistema operativo**: Linux (Ubuntu, Amazon Linux, Debian, CentOS) o Windows
- **Hardware virtual**: CPU, RAM, tipo de almacenamiento
- **Red**: Qué VPC, qué subred, qué dirección IP
- **Seguridad**: Qué puertos están abiertos, quién puede acceder
- **Software**: Qué aplicaciones instalar una vez creado el servidor

La palabra "Elastic" en el nombre se refiere a la capacidad de escalar hacia arriba o hacia abajo fácilmente. Puedes tener 1 instancia o 100, y puedes cambiarlas de tamaño según necesites.

### Componentes de una instancia EC2

Cuando creas una instancia EC2, necesitas tomar decisiones sobre varios componentes:

**1. AMI (Amazon Machine Image)**

La AMI es la plantilla que define el sistema operativo y el software preinstalado. AWS proporciona muchas AMIs oficiales:

- **Amazon Linux 2023**: Linux optimizado para AWS, gratuito
- **Ubuntu Server 22.04 LTS**: Distribución Linux popular, gratuito
- **Microsoft Windows Server**: Para ejecutar aplicaciones Windows, de pago por minuto
- **Red Hat Enterprise Linux**: Enterprise Linux, de pago

También existen AMIs de la comunidad y de mercado con software preconfigurado.

**2. Tipo de instancia**

El tipo de instancia define la combinación de CPU, memoria, almacenamiento y capacidad de red. AWS ofrece docenas de tipos organizados en familias:

| Familia | Propósito | Ejemplos |
|---------|-----------|----------|
| **t** (Burstable) | Uso general, económico | t3.micro, t3.small |
| **m** (General Purpose) | Más potencia que t | m5.large, m5.xlarge |
| **c** (Compute Optimized) | Mucha CPU | c5.large, c5.2xlarge |
| **r** (Memory Optimized) | Mucha RAM | r5.large, r5.xlarge |

Para aprender y desarrollo, las instancias **t3.micro** o **t3.small** son ideales porque son gratuitas dentro del tier de uso gratuito de AWS.

**3. Configuración de red (VPC y subred)**

La VPC define la red virtual donde vivirá tu instancia. La subred determina si la instancia tiene una IP pública (accesible desde internet) o solo privada.

Para una primera práctica simple, puedes usar la VPC por defecto que AWS crea automáticamente en cada cuenta.

**4. IP Pública**

Por defecto, las instancias en una subred pública reciben una IP pública automáticamente. Esta IP te permite conectarte desde internet.

También puedes usar un Elastic IP (IP fija que no cambia) pero tiene coste aunque no la uses.

**5. Almacenamiento (EBS)**

EBS (Elastic Block Store) es el sistema de almacenamiento para instancias EC2. Es como un disco duro virtual.

Opciones comunes:

- **gp3**: SSD de propósito general, el más común, 3000 IOPS base
- **gp2**: SSD de propósito general, más antiguo
- **io2**: SSD de alto rendimiento para bases de datos
- **st1**: HDD de bajo coste para almacenamiento masivo
- **sc1**: HDD de menor coste aún

El tamaño por defecto es 8GB o 10GB para muchas AMIs. Puedes aumentarlo.

**6. Security Group (Grupo de seguridad)**

El Security Group actúa como un firewall virtual para tu instancia. Controla qué tráfico puede entrar y salir.

Por ejemplo, puedes definir:

- Permitir SSH (puerto 22) desde tu IP
- Permitir HTTP (puerto 80) desde cualquier lugar
- Permitir HTTPS (puerto 443) desde cualquier lugar

**7. Key Pair (Par de claves)**

Para conectarte a una instancia Linux, necesitas un par de claves SSH. Consiste en:

- **Clave pública**: Se instala en la instancia durante la creación
- **Clave privada**: Tú la descargas y guardas securely. Es la única forma de conectarte

**Nunca pierdas tu clave privada**. Si la pierdes, no podrás acceder a instancias creadas con ella.

---

## Tipos de instancias EC2

Elegir el tipo de instancia correcto es importante para balancear rendimiento y coste. Aquí una guía más detallada.

### Familia T: Burstable Performance

Las instancias T son económicas y adecuadas para workloads con uso moderado que tienen picos ocasionales.

| Tipo | vCPU | RAM (GB) | Coste/hora* |
|------|------|----------|-------------|
| t3.micro | 2 | 1 | $0.0104 |
| t3.small | 2 | 2 | $0.0208 |
| t3.medium | 2 | 4 | $0.0416 |
| t3.large | 2 | 8 | $0.0832 |

*Precios en us-east-1, Linux, On-Demand. Pueden cambiar.

**Burstable significa que si tu servidor no está usando toda su CPU, acumula "creditos de CPU". Cuando tienes un pico de trabajo, usa esos créditos para burst (explotar) por encima de su capacidad base.

### Familia M: General Purpose

Más potencia sostenida que las T. Buenas para aplicaciones de propósito general.

| Tipo | vCPU | RAM (GB) | Coste/hora* |
|------|------|----------|-------------|
| m5.large | 2 | 8 | $0.096 |
| m5.xlarge | 4 | 16 | $0.192 |

### Familia C: Compute Optimized

Mucha CPU. Ideales para computational intensive workloads como HPC, machine learning, o servidores de gaming.

| Tipo | vCPU | RAM (GB) | Coste/hora* |
|------|------|----------|-------------|
| c5.large | 2 | 4 | $0.085 |
| c5.xlarge | 4 | 8 | $0.17 |

### Familia R: Memory Optimized

Mucha RAM. Para bases de datos, caches en memoria, big data analytics.

| Tipo | vCPU | RAM (GB) | Coste/hora* |
|------|------|----------|-------------|
| r5.large | 2 | 16 | $0.126 |
| r5.xlarge | 4 | 32 | $0.252 |

### ¿Qué tipo usar para qué?

**Para aprender y prácticas**: `t3.micro` o `t3.small`. Son gratuitas en el tier de uso gratuito de AWS (750 horas/mes durante 12 meses para cuentas nuevas).

**Para un servidor web pequeño**: `t3.small` o `t3.medium` dependiendo del tráfico.

**Para desarrollo con varias aplicaciones**: `t3.medium` o `m5.large`.

**Para producción con tráfico moderado**: `m5.large` o superior, distribuido across varias instancias.

### ¿Qué es el tier gratuito de AWS?

AWS ofrece un tier gratuito (Free Tier) para cuentas nuevas:

**Always Free**: Algunos servicios son siempre gratuitos:

- AWS Lambda: 1M de peticiones gratis al mes
- DynamoDB: 25 GB de almacenamiento
- CloudWatch: 10 dashboards al mes, 5 GB de logs al mes

**12 Months Free**: Disponible durante 12 meses desde la creación de la cuenta:

- EC2: 750 horas de t2.micro o t3.micro por mes
- S3: 5 GB de almacenamiento estándar
- RDS: 750 horas de db.t2.micro o db.t3.micro

**Es importante**: Si excedes estos límites, empezarás a pagar. Lee siempre los precios antes de crear recursos.

---

## Creando tu primera instancia EC2

Vamos a crear una instancia EC2 paso a paso. Asumimos que ya tienes acceso a la consola de AWS.

### Paso 1: Acceder al servicio EC2

1. En la consola de AWS, busca "EC2" en el buscador de servicios o navega a través del menú
2. Una vez en el panel de EC2, busca el botón azul "Launch instance" o "Lanzar instancia"

### Paso 2: Nombrar la instancia

1. En el campo "Name", escribe un nombre descriptivo: `mi-primera-instancia`
2. Este nombre aparecerá como etiqueta (tag) en la instancia y facilita identificarla

### Paso 3: Elegir la AMI

1. En la sección "AMI", ver&aring;s una lista de AMIs disponibles
2. Para empezar, busca "Ubuntu Server 22.04 LTS (Free tier eligible)" o "Amazon Linux 2023 (Free tier eligible)"
3. Click en "Select" o en la AMI que elijas

**Recomendación para principiantes**: Ubuntu Server es una buena elección porque:

- Es muy popular y hay mucha documentación
- Es similar a otros sistemas Linux que probablemente conozcas
- La comunidad es activa y hay muchos tutoriales

### Paso 4: Elegir el tipo de instancia

1. En "Instance type", ver&aring;s el tipo preseleccionado (generalmente t2.micro o t3.micro)
2. Asegúrate de que dice "Free tier eligible"
3. Si quieres otra cosa, seleciona el tipo del menú desplegable
4. Para aprender, `t3.micro` es más que suficiente

### Paso 5: Configurar detalles de red

1. Por ahora, usa los valores por defecto que aparecerán
2. Si quieres profundizar más tarde, puedes elegir:
   - **VPC**: La red virtual donde se creará la instancia
   - **Subnet**: La zona de disponibilidad específica
   - **Auto-assign public IP**: Activa esto si quieres que la instancia tenga IP pública (necesario para SSH desde internet)

### Paso 6: Agregar almacenamiento

1. En la sección "Storage", ver&aring;s el volumen raíz (generalmente 8GB o 10GB para Ubuntu)
2. Puedes cambiar el tamaño o añadir más volúmenes
3. Para empezar, los valores por defecto están bien
4. El volumen gp3 es el más común actualmente

### Paso 7: Configurar advanced details (opcional)

Expandiendo "Advanced details" tienes opciones adicionales:

- **IAM role**: Para dar permisos a la instancia (para scripts que acceden a otros servicios AWS)
- **User data**: Script que se ejecuta al iniciar la instancia (útil para instalar software automáticamente)
- **Termination protection**: Protege contra termination accidental

Para una primera práctica, puedes dejarlo todo por defecto.

### Paso 8: Añadir etiquetas (Tags)

1. En la sección "Tags", puedes añadir etiquetas para organizar recursos
2. Click en "Add tag":
   - Key: `Environment`
   - Value: `desarrollo`
3. O simplemente usa el tag de Name que ya pusiste

### Paso 9: Configurar el Security Group

1. En la sección "Security Group", defines las reglas de firewall
2. Por defecto, verás algo como:
   - **Type**: SSH
   - **Protocol**: TCP
   - **Port Range**: 22
   - **Source**: Anywhere (o tu IP si seleccionaste esa opción)

3. Para desarrollo, está bien permitir SSH desde "My IP" para mayor seguridad, o "Anywhere" si quieres poder conectarte desde cualquier lugar (cuidado en producción)

4. **Importante**: SSH está bien para aprender, pero en producción deberías usar una VPN o AWS Direct Connect.

### Paso 10: Revisar y lanzar

1. Aparecerá un resumen de todas tus selections
2. Revisa que todo está correcto
3. Click en "Launch"

### Paso 11: Seleccionar o crear Key Pair

1. Al hacer click en Launch, AWS te pedir&aacute; que selecciones un Key Pair
2. **Opción A**: Crear uno nuevo:
   - Click en "Create new key pair"
   - Nombre: `mi-clave-aws` (o el nombre que prefieras)
   - Click en "Download key pair"
   - **GUARDA EL ARCHIVO .pem en un lugar seguro**
3. **Opción B**: Usar uno existente:
   - Si ya tienes un key pair creado, selecciónalo

4. **MUY IMPORTANTE**: Sin la clave privada, NO podrás conectarte a tu instancia. Guárdala bien.

5. Checkbox: "I acknowledge that..." (reconozco que sin la clave no podré acceder)
6. Click en "Launch Instances"

### Paso 12: Esperar a que la instancia esté corriendo

1. AWS te mostrará un mensaje de éxito
2. Click en "View instance" para ver tu nueva instancia
3. Verás la instancia en la lista. Su estado inicial será "Pending"
4. En 30-60 segundos, cambiará a "Running"
5. Cuando esté corriendo, verás:
   - **Instance ID**: `i-0abc123def456789`
   - **Public IPv4 address**: `54.123.456.789` (anótala, la necesitarás)
   - **Instance state**: Running

**¡Felicidades! Acabas de crear tu primer servidor en la nube.**

---

## Grupos de seguridad: el firewall de AWS

Un Security Group actúa como un firewall virtual para tu instancia EC2 y otros recursos. Es absolutamente fundamental entender cómo funcionan.

### Cómo funcionan los Security Groups

Los Security Groups tienen una lógica de "permitir solo lo explícitamente permitido". Por defecto:

- **Todo el tráfico entrante está DENEGADO** (a menos que lo permitas)
- **Todo el tráfico saliente está PERMITIDO**

Cada regla que añades es una regla de "permitir". No hay reglas de denegar explícitas (para eso están los NACLs, pero eso es más avanzado).

### Componentes de una regla de Security Group

Cada regla tiene:

- **Type**: El tipo de tráfico (SSH, HTTP, HTTPS, All Traffic, Custom, etc.)
- **Protocol**: TCP, UDP, ICMP, o All
- **Port range**: Puerto o rango de puertos (ej: 22, 80, 5000-6000)
- **Source/Destination**:
  - IP específica (ej: 192.168.1.1/32)
  - Rango CIDR (ej: 10.0.0.0/16)
  - Otro Security Group (permite tráfico desde instancias con ese SG)
  - "My IP" (tu IP pública actual)
  - "Anywhere-IPv4" (0.0.0.0/0) - CUIDADO, permite a cualquiera

### Security Groups comunes

**Security Group para servidor web básico:**

```
Entrada:
- SSH (22) desde My IP (solo tú puedes conectar)
- HTTP (80) desde Anywhere (tráfico web normal)
- HTTPS (443) desde Anywhere (tráfico web cifrado)

Salida:
- Todo (0.0.0.0/0) - La instancia puede conectarse a internet libremente
```

**Security Group para base de datos (solo acceso interno):**

```
Entrada:
- MySQL/Aurora (3306) desde Security Group de aplicación (solo servidores de app pueden conectar)

Salida:
- Todo (0.0.0.0/0)
```

### Editar Security Groups

Puedes modificar los Security Groups de una instancia:

1. En la lista de instancias, click en la instancia
2. En la pestaña "Security", ver&aring;s los Security Groups asociados
3. Click en el link al Security Group o en "Edit inbound rules" / "Edit outbound rules"

### Ejemplo: Añadir regla para HTTP

1. Click en "Edit inbound rules"
2. Click en "Add rule"
3. Rellena:
   - Type: HTTP
   - Port: 80 (automático para HTTP)
   - Source: Anywhere-IPv4 (0.0.0.0/0)
4. Click en "Save rules"

### Errores comunes con Security Groups

**Error: "Connection timed out"**

Significa que el tráfico está siendo bloqueado por el Security Group o el firewall del sistema operativo. Verifica que el Security Group permite el tráfico que necesitas.

**Error: "Connection refused"**

Significa que el Security Group permite el tráfico, pero no hay nada escuchando en ese puerto. Verifica que el servicio (nginx, apache, etc.) está corriendo.

**Abrir SSH (22) a Anywhere**

Es un riesgo de seguridad. En producción, limita siempre SSH a tu IP o a un rango de IPs de confianza.

### Buenas prácticas con Security Groups

1. **Principio de mínimo privilegio**: Solo abre los puertos que necesites
2. **Usa grupos en lugar de IPs**: Para comunicación entre instancias, permite el Security Group de la otra en lugar de IPs específicas
3. **Nombra descriptivamente**: `web-servers-sg`, `database-sg`, `app-servers-sg`
4. **Documenta las reglas**: Añade descripciones a cada regla explicando para qué sirve
5. **Revisa periódicamente**: Auditoría de qué puertos están abiertos

---

## Conectándose a EC2 mediante SSH

SSH (Secure Shell) es el protocolo que te permite conectarte remotamente a servidores Linux. Es la forma estándar de administrar servidores en la nube.

### ¿Qué es SSH?

SSH es un protocolo加密 que permite conexiones seguras sobre redes no seguras. Cuando te conectas a tu instancia EC2 por SSH, toda la comunicación entre tu ordenador y el servidor está cifrada.

Sin SSH, tendrías que acceder al servidor físicamente (imposible si está en un datacenter a miles de kilómetros) o a través de una interfaz web menos práctica.

### Prerrequisitos para conectar por SSH

Antes de poder conectarte, necesitas:

1. **Una instancia EC2 corriendo**: Con estado "Running"
2. **Un Security Group que permita SSH** (puerto 22) desde tu IP
3. **La clave privada (.pem)**: Que descargaste al crear la instancia
4. **La IP pública de la instancia**: En formato como `54.123.456.789`
5. **Un cliente SSH**: En Linux y macOS ya viene instalado; en Windows puedes usar PowerShell, Git Bash, o Windows Subsystem for Linux (WSL)

### Diferencia entre usuario según AMI

Según la AMI que hayas elegido, el usuario SSH es diferente:

| AMI | Usuario SSH |
|-----|------------|
| Amazon Linux | `ec2-user` |
| Ubuntu | `ubuntu` |
| Debian | `admin` o `root` |
| RHEL | `ec2-user` o `root` |
| Fedora | `ec2-user` o `fedora` |
| SUSE | `ec2-user` o `root` |

Para Ubuntu Server, el usuario es `ubuntu`.

### Conectarse desde Linux o macOS

**Paso 1: Asegúrate de que tu clave tiene los permisos correctos**

Antes de usar la clave, necesitas asegurarte de que tiene los permisos correctos (solo tú puedes leerla):

```bash
chmod 400 /ruta/a/tu-clave.pem
```

**Paso 2: Conectar**

Abre una terminal y ejecuta:

```bash
ssh -i /ruta/a/tu-clave.pem ubuntu@54.123.456.789
```

Explicación:

- `ssh`: El comando de SSH
- `-i /ruta/a/tu-clave.pem`: Indica cuál es tu clave privada
- `ubuntu`: El nombre de usuario
- `@`: Separador
- `54.123.456.789`: La IP pública de tu instancia

**Paso 3: Aceptar la clave de host**

La primera vez que te conectes, SSH te preguntará:

```
The authenticity of host '54.123.456.789 (54.123.456.789)' can't be established.
ECDSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no)?
```

Escribe `yes` y presiona Enter. Esto añade el servidor a tu lista de hosts conocidos.

**Paso 4: Deberías ver la terminal del servidor**

Si todo fue bien, verás algo como:

```
ubuntu@ip-10-0-1-123:~$
```

¡Estás dentro! El prompt muestra `ubuntu@...` indicando que eres el usuario ubuntu en ese servidor.

### Conectarse desde Windows

**Opción A: Windows Subsystem for Linux (WSL)**

Si tienes WSL instalado (Ubuntu, Debian, etc.):

1. Abre Ubuntu o tu distribución Linux en WSL
2. Copia tu archivo .pem a WSL (puedes acceder a los archivos de Windows desde `/mnt/c/`)
3. Sigue los pasos de Linux/macOS

**Opción B: PowerShell**

1. Abre PowerShell
2. Asegúrate de que tienes SSH instalado (en Windows 10/11 generalmente ya viene)
3. Los pasos son similares a Linux:

```powershell
ssh -i .\tu-clave.pem ubuntu@54.123.456.789
```

**Opción C: Git Bash**

1. Descarga e instala Git Bash desde https://git-scm.com
2. Abre Git Bash
3. Los pasos son similares a Linux:

```bash
ssh -i /ruta/a/tu-clave.pem ubuntu@54.123.456.789
```

**Opción D: PuTTY**

PuTTY es un cliente SSH clásico para Windows, pero requiere convertir la clave .pem a formato .ppk:

1. Descarga PuTTYgen
2. Carga tu archivo .pem
3. Save as private key
4. Abre PuTTY
5. En Host Name: `ubuntu@54.123.456.789`
6. En Connection > SSH > Auth: carga tu archivo .ppk
7. Click Open

### Problemas comunes de conexión

**"Permission denied (publickey)"**

Esto significa que la autenticación con clave SSH falló. Causas posibles:

1. **Ruta incorrecta a la clave**: Verifica que la ruta al archivo .pem es correcta
2. **Permisos incorrectos en la clave**: Asegúrate de haber hecho `chmod 400`
3. **Clave incorrecta**: Si descargaste otra clave o la instancia se creó con otra clave, no funcionará
4. **Usuario incorrecto**: Verifica que usas el usuario correcto según la AMI

**"Connection timed out"**

El tráfico SSH está siendo bloqueado. Causas posibles:

1. **El Security Group no permite SSH desde tu IP**: Edita el Security Group y permite SSH desde "My IP"
2. **La instancia no tiene IP pública**: Verifica en los detalles de la instancia que tiene una IP pública
3. **La instancia está en una subred privada**: Las instancias en subredes privadas sin NAT no son accesibles desde internet

**"No route to host"**

Similar a connection timed out. Verifica networking y que la IP es correcta.

### Ya estoy conectado, ¿qué ahora?

¡Bienvenido a tu servidor! Ahora puedes:

**Explorar el sistema:**

```bash
# Ver qué sistema operativo tienes
cat /etc/os-release

# Ver información del hardware
cat /proc/cpuinfo | head -20
free -h
df -h

# Ver información de red
ip addr
hostname -I
```

**Actualizar el sistema (importante al comenzar):**

```bash
sudo apt update && sudo apt upgrade -y
```

**Instalar software:**

```bash
# Instalar Nginx (servidor web)
sudo apt install nginx -y

# Instalar Node.js
sudo apt install nodejs npm -y

# Instalar Python
sudo apt install python3 python3-pip -y
```

**Ver logs:**

```bash
# Ver logs del sistema
sudo journalctl -f

# Ver logs de nginx
sudo tail -f /var/log/nginx/access.log
```

### Cerrar la conexión

Cuando termines, simplemente:

```bash
exit
```

O presiona `Ctrl+D`.

---

## Gestión de claves SSH

Las claves SSH son fundamentales para la seguridad de tus instancias EC2. Vamos a profundizar en cómo gestionarlas.

### Cómo funcionan las claves SSH con EC2

Cuando creas un par de claves en EC2:

1. **AWS almacena la clave pública** en la instancia durante su creación
2. **Tú descargas y guardas la clave privada** (archivo .pem)
3. **Para conectarte**, usas la clave privada que debe coincidir con la pública en el servidor

Esto es criptografía asimétrica:

- **Lo que cifras con la pública, solo se puede descifrar con la privada**
- **Lo que firmas con la privada, cualquiera puede verificar con la pública**

### Crear un par de claves EC2

Puedes crear un par de claves desde la consola:

1. En el panel de EC2, navega a "Key Pairs" en el menú izquierdo
2. Click en "Create key pair"
3. Dale un nombre: `mi-clave-persistente`
4. Tipo: RSA
5. Formato: .pem (para Linux/Mac) o .ppk (para PuTTY)
6. Click en "Create"
7. Descarga automáticamente el archivo .pem

### Crear clave SSH localmente

También puedes crear un par de claves en tu ordenador y solo importar la clave pública a AWS:

**En Linux/macOS:**

```bash
# Crear clave RSA de 4096 bits
ssh-keygen -t rsa -b 4096 -C "mi-email@ejemplo.com"

# Te preguntará dónde guardarla, pulsa Enter para aceptar la ubicación por defecto
# Te preguntará una contraseña (passphrase), puedes dejarla vacía o poner una

# Ver tu clave pública
cat ~/.ssh/id_rsa.pub
```

**Importar a AWS:**

1. En el panel de EC2, "Key Pairs"
2. Click en "Actions" > "Import key pair"
3. Dale un nombre
4. Pega el contenido de tu clave pública
5. Click en "Import"

Ahora puedes usar tu clave local existente para conectarte a instancias AWS.

### La importancia de guardar tu clave privada

**NUNCA pierdas tu clave privada**. Si la pierdes:

- **Para instancias nuevas**: Simplemente crea una nueva instancia con una nueva clave
- **Para instancias existentes**: Si no tienes acceso a la clave original y no configuraste una forma alternativa de acceso, **no podrás acceder a la instancia**. AWS no puede recuperarte la clave.

**Para recuperación**, tendrías que:

1. Detener la instancia
2. Separar el volumen EBS
3. Adjuntar el volumen a otra instancia donde tengas acceso
4. Montar el volumen y modificar authorized_keys
5. Volver a adjuntar el volumen a la instancia original

Es un proceso tedioso, así que mejor no perder la clave.

### Guardar la clave en un lugar seguro

En Linux/macOS:

```bash
# Ubicación recomendada: ~/.ssh/
mkdir -p ~/.ssh
mv ~/Downloads/mi-clave.pem ~/.ssh/
chmod 400 ~/.ssh/mi-clave.pem
```

**Nunca** guardes claves privadas en:

- Repositorios Git
- Dropbox, Google Drive u otras nubes públicas
- Carpetas compartidas
- Correo electrónico

### Usar SSH config para múltiples servidores

Si trabajas con varias instancias, puedes configurar SSH para no tener que recordar todas las IPs y claves:

Edita o crea `~/.ssh/config`:

```
Host mi-servidor-web
    HostName 54.123.456.789
    User ubuntu
    IdentityFile ~/.ssh/mi-clave.pem

Host mi-servidor-db
    HostName 54.234.567.890
    User ubuntu
    IdentityFile ~/.ssh/mi-clave.pem
```

Ahora simplemente haz:

```bash
ssh mi-servidor-web
```

### Rotación de claves

Por seguridad, es buena práctica rotar (cambiar) las claves periódicamente:

1. Crea un nuevo par de claves en AWS
2. Conecta a la instancia con la clave antigua
3. Añade la nueva clave pública a `~/.ssh/authorized_keys`
4. Verifica que puedes conectar con la nueva clave
5. Elimina la clave antigua de `authorized_keys`
6. Elimina el par de claves antiguo de AWS (ya no es necesario si no tienes instancias usándolo)

### Diferentes claves para diferentes entornos

Una buena práctica es usar diferentes claves para diferentes entornos:

- **Clave de desarrollo**: Para instancias de desarrollo
- **Clave de producción**: Para instancias de producción (más restrictiva)

Esto te permite revocar la clave de desarrollo sin afectar producción, y aplicar diferentes políticas de seguridad.

---

## Almacenamiento: EBS y S3

AWS ofrece diferentes servicios de almacenamiento para diferentes casos de uso. Los dos más importantes para empezar son EBS y S3.

### Amazon EBS (Elastic Block Store)

EBS proporciona almacenamiento en bloques para instancias EC2. Es como un disco duro virtual que se adjunta a tu instancia.

**Características:**

- **Persistente**: Los datos sobreviven si la instancia se detiene o termina (si el volumen está configurado para ello)
- **Rendimiento específico**: Diferentes tipos de volúmenes ofrecen diferentes niveles de IOPS (operaciones de entrada/salida por segundo)
- **Cifrado**: Soporta cifrado AES-256
- **Snapshots**: Puedes hacer backups (snapshots) a S3

**Tipos de volúmenes EBS:**

| Tipo | Uso | Precio relativo |
|------|-----|-----------------|
| **gp3** | Propósito general, SSD | Medio |
| **gp2** | Propósito general, SSD (más antiguo) | Medio |
| **io2** | Alto rendimiento, SSD | Alto |
| **st1** | HDD de bajo coste para throughput | Bajo |
| **sc1** | HDD de muy bajo coste | Muy bajo |

**gp3** es generalmente la mejor elección para la mayoría de workloads por su equilibrio entre coste y rendimiento.

**Administrar volúmenes EBS:**

```bash
# Ver discos disponibles
lsblk

# Ver espacio en disco
df -h

# Ver información del volumen (no montados)
sudo lsbock
```

### Amazon S3 (Simple Storage Service)

S3 es almacenamiento de objetos, diferente a EBS. Es más como un sistema de archivos infinito donde guardas archivos (objetos) en buckets.

**Características:**

- **global**: Los buckets son globales, pero puedes restringir acceso por región
- **Escalabilidad automática**: No hay límite práctico de capacidad
- **Muy duradero**: 99.999999999% (once nueves)
- **Versiones**: Puede mantener múltiples versiones de un archivo
- **Lifecycle policies**: Automatizar la transición a clases de almacenamiento más baratas

**Clases de almacenamiento S3:**

| Clase | Uso | Precio |
|-------|-----|--------|
| **S3 Standard** | Datos frecuentemente accedidos | Medio |
| **S3 Intelligent-Tiering** | Datos con patrones de acceso impredecibles | Variable |
| **S3 Standard-IA** | Datos menos frecuentes pero que necesitan acceso rápido | Menor |
| **S3 Glacier** | Archivos que raramente se accesan, retrieval en minutos a horas | Muy bajo |

**Buckets y objetos:**

Un bucket es como un directorio de nivel superior. Dentro puedes crear "carpetas" lógicas (aunque técnicamente S3 es flat):

```
mi-bucket/
├── imagenes/
│   ├── logo.png
│   └── screenshot.jpg
└── documentos/
    └── informe.pdf
```

**Crear un bucket S3:**

1. En la consola de AWS, busca "S3"
2. Click en "Create bucket"
3. Dale un nombre único globalmente (ej: `mi-bucket-unico-12345`)
4. Selecciona la región
5. Las opciones por defecto están bien para empezar
6. Click en "Create bucket"

**Subir archivos a S3:**

1. Entra en el bucket
2. Click en "Upload"
3. Arrastra archivos o click en "Add files"
4. Click en "Upload"

**Acceder a objetos:**

Los objetos en buckets públicos tienen URLs como:

```
https://mi-bucket.s3.amazonaws.com/imagenes/logo.png
```

### ¿Cuándo usar EBS vs S3?

| Aspecto | EBS | S3 |
|---------|-----|-----|
| **Qué almacena** | Discos para instancias | Archivos sueltos |
| **Acceso** | Como disco duro (archivos, bases de datos) | Como URLs o API |
| **Precio** | Por GB/month + IOPS | Por GB/month + requests |
| **Persistencia** | Hasta que lo borres | Indefinido |
| **Acceso desde instancia** | Sí, como disco | Sí, como API o mount |

**Ejemplo:**

- **EBS**: El disco raíz de tu instancia EC2, volume para base de datos
- **S3**: Imágenes de perfil de usuarios, logs exportados, archivos estáticos de web, backups

---

## Redes básicas: VPC simplificado

VPC (Virtual Private Cloud) es el servicio de redes de AWS. Permite crear redes privadas virtuales en la nube.

### VPC por defecto

Cuando creas una cuenta de AWS, se crea automáticamente una VPC por defecto en cada región. Esta VPC incluye:

- Un bloque CIDR (rango de IPs) como 172.31.0.0/16
- Una gateway de internet
- Tablas de enrutamiento básicas
- Security Groups por defecto
- Network ACLs por defecto

Para la mayoría de prácticas de aprendizaje, puedes usar esta VPC por defecto sin preocuparte por crear una personalizada.

### Conceptos básicos de VPC

**CIDR Block**: El rango de direcciones IP privadas en la VPC. Por ejemplo, 10.0.0.0/16 significa que tienes 65,536 direcciones IP disponibles (10.0.0.0 a 10.0.255.255).

**Subred**: Una subdivisión de la VPC. Por ejemplo, dividiendo 10.0.0.0/16 en dos subredes:

- 10.0.0.0/24 (256 IPs: 10.0.0.0 a 10.0.0.255)
- 10.0.1.0/24 (256 IPs: 10.0.1.0 a 10.0.1.255)

**Subred pública vs privada**:

- **Pública**: Tiene ruta directa a internet (a través de Internet Gateway)
- **Privada**: No tiene ruta directa a internet. Para salir a internet, usa NAT Gateway o NAT Instance

**Internet Gateway**: El componente que permite a recursos en la VPC acceder a internet.

**Route Table**: Define hacia dónde va el tráfico. Cada subred tiene una tabla de enrutamiento.

### ¿Qué configuración tiene mi instancia por defecto?

Cuando creas una instancia EC2 en la consola:

- Se crea en la VPC por defecto
- En una subred de la VPC por defecto (generalmente la primera)
- Si la subred es pública, recibe IP pública automáticamente
- Se le aplica el Security Group que configures

### Ejemplo simple de arquitectura

```
Internet
    │
    ▼
┌─────────────────────────────┐
│        Internet Gateway       │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│     VPC: 10.0.0.0/16        │
│                             │
│  ┌───────────────────────┐  │
│  │  Subred pública       │  │
│  │  10.0.0.0/24           │  │
│  │                       │  │
│  │  [EC2 Instance]       │  │─── Security Group: SSH (22), HTTP (80)
│  │  IP: 10.0.0.10        │  │
│  │  Public IP: 54.x.x.x  │  │
│  └───────────────────────┘  │
│                             │
│  ┌───────────────────────┐  │
│  │  Subred privada       │  │
│  │  10.0.1.0/24           │  │
│  │                       │  │
│  │  [RDS Database]       │  │
│  │  IP: 10.0.1.10        │  │
│  │  (No IP pública)      │  │
│  └───────────────────────┘  │
│                             │
└─────────────────────────────┘
```

En este ejemplo:

- El servidor EC2 en la subred pública puede recibir tráfico de internet y también acceder a internet
- La base de datos RDS en la subred privada no es accesible directamente desde internet
- El servidor EC2 puede conectar a la base de datos porque están en la misma VPC

### Para profundizar

VPC es un tema muy amplio. Una vez domines lo básico de EC2,回来 aprender:

- Crear VPCs personalizadas con rangos de IP específicos
- Configurar subredes públicas y privadas
- Usar NAT Gateway para permitir a instancias privadas acceder a internet
- Configurar VPN o Direct Connect para conectar redes on-premises
- VPC Peering para comunicar VPCs entre sí
- Security Groups vs Network ACLs (NACLS)

---

## Costes y economía de AWS

Entender cómo AWS cobra por sus servicios es importante para evitar sorpresas en la factura.

### Cómo AWS cobra por EC2

EC2 se cobra por hora de uso, dependiendo de:

1. **Tipo de instancia**: t3.micro es más barato que m5.large
2. **Sistema operativo**: Linux es más barato que Windows (Windows incluye licencias de Microsoft)
3. **Región**: Los precios varían entre regiones
4. **Modelo de precio**:
   - **On-Demand**: Pagas por hora sin compromiso
   - **Reserved**: Descuento por compromiso de 1-3 años
   - **Spot**: Descuento muy alto (hasta 90%) por instancias que pueden ser interrumpidas

**Ejemplo de precios t3.micro en us-east-1 (Linux):**

| Modelo | Precio/hora |
|--------|-------------|
| On-Demand | $0.0104 |
| 1 year Reserved (sin upfront) | $0.006 |
| 1 year Reserved (all upfront) | $0.005 |
| Spot | $0.002 - $0.004 (variable) |

### Otros costes asociados a EC2

Además de la instancia en sí, hay costes adicionales:

- **EBS Storage**: ~$0.08/GB-month para gp3
- **EBS I/O**: Los volúmenes gp3 tienen IOPS incluidas, gp2 cobra por IOPS extra
- **Data Transfer**: Trasferencia de datos entre AZs, regiones, o fuera de AWS
- **Elastic IPs**: Gratis si la usas, $0.005/hora si la reservas y no la usas

### Servicios con coste gratuito

Algunos servicios son gratuitos dentro de límites:

- **CloudWatch Basic Monitoring**: Metrics para EC2 cada 5 minutos (no detallado)
- **S3**: 5 GB de almacenamiento estándar el primer año
- **CloudFront**: 1TB de transferencia de datos al mes
- **Lambda**: 1M de peticiones y 400,000 GB-segundos de computación al mes

### Herramientas para gestionar costes

**AWS Budgets**: Te permite definir presupuestos y alertas cuando los costes alcancen ciertos umbrales.

**Cost Explorer**: Visualiza y analiza tus costes históricos.

**Cost Allocation Tags**: Etiquetas que te permiten desglosar costes por proyecto, entorno, etc.

### Estimar costes antes de crear

Antes de crear recursos, usa la **Calculadora de Precios de AWS**:

1. Ve a https://calculator.aws
2. Selecciona los servicios que planeas usar
3. Especifica configuración (tipo de instancia, almacenamiento, transferencia, etc.)
4. Obtén una estimación mensual

**Ejemplo rápido para t3.micro:**

| Recurso | Cantidad | Precio estimado/mes |
|---------|----------|---------------------|
| EC2 t3.micro (Linux) | 1 | ~$7.50 (720 horas) |
| EBS gp3 20GB | 1 | ~$1.60 |
| Transferencia 1GB | 1 GB | ~$0.09 |
| **Total** | | **~$9.19** |

### Consejos para ahorrar en AWS Academy

**Monitorea tu uso**: Revisa el dashboard de AWS Academy regularmente para ver cuánto has usado.

**Usa el tier gratuito**: t3.micro está dentro del tier gratuito (750 horas/mes).

**Detén instancias cuando no las uses**: Si no necesitas la instancia por unos días, simplemente Stop. No cobran por instancias detenidas, solo por el almacenamiento EBS.

**Elimina recursos temporales**: Si creaste recursos para una práctica, elimínalos cuando termines.

**Cuidado con los Elastic IPs**: Si reservas una IP elástica y no la asignas a una instancia, te cobran por cada hora que no la uses.

---

## Buenas prácticas de seguridad

La seguridad en AWS es responsabilidad compartida entre AWS y tú. AWS es responsable de la seguridad "de la nube", tú de la seguridad "en la nube".

### Principios fundamentales

**Principio de mínimo privilegio**: Solo da los permisos estrictamente necesarios. No uses el usuario root de AWS para trabajo diario. Crea usuarios IAM con permisos específicos.

**Defensa en profundidad**: No confíes en una sola capa de seguridad. Usa múltiples capas: Security Groups, NACLS, IAM, cifrado, etc.

**Todo registra y monitoriza**: Usa CloudWatch Logs, AWS CloudTrail (registra llamadas a la API), y configura alarmas.

### Seguridad para instancias EC2

**1. Usa key pairs, nunca passwords**

Nunca habilites password authentication en SSH. Usa siempre claves SSH.

**2. Mantén el sistema actualizado**

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Actualizar solo seguridad
sudo apt update && sudo apt upgrade -y security
```

**3. Instala solo lo necesario**

Cada servicio instalado es una superficie de ataque potencial. Instala solo lo que necesites.

**4. Usa usuarios normales, no root**

```bash
# Crear usuario
sudo adduser deploy

# Añadir a sudo
sudo usermod -aG sudo deploy

# Luego ssh como deploy y usa sudo cuando necesites
```

**5. Configura Firewall del SO**

Además del Security Group de AWS, puedes usar ufw (Uncomplicated Firewall) en Linux:

```bash
# Instalar ufw
sudo apt install ufw

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activar
sudo ufw enable
```

### Seguridad de la cuenta AWS

**1. Activa MFA en tu cuenta root**

El usuario root (el email con el que creaste la cuenta) tiene todos los permisos. Protégelo con MFA (autenticación de múltiples factores).

**2. No uses credenciales root para trabajo diario**

Crea un usuario IAM con permisos de administrador o los permisos específicos que necesites.

**3. Rota credenciales**

Si usas access keys (para API/CLI), rotalas periódicamente.

**4. Revisa permisos de IAM**

Periódicamente, audita qué usuarios tienen qué permisos y elimina lo que no sea necesario.

### Security Groups seguros

**No**:

- SSH desde Anywhere (0.0.0.0/0)
- Abrir puertos de base de datos (3306, 5432) a internet

**Sí**:

- SSH desde tu IP específica o un rango conocido
- Puertos de aplicación (80, 443) desde Anywhere si son servicios públicos legítimos
- Puertos de base de datos solo desde Security Groups de aplicaciones confiables

### Datos sensibles

**Nunca hardcodees secrets en código**

Si necesitas guardar contraseñas, API keys, tokens:

- Usa AWS Secrets Manager
- Usa AWS Systems Manager Parameter Store
- Usa variables de entorno
- Nunca en código fuente o archivos de configuración en repositorios

**Cifra datos sensibles**

- EBS supports cifrado
- S3 supports cifrado (SSE-S3, SSE-KMS)
- RDS supports cifrado en reposo

---

## Glosario de términos AWS

| Término | Definición |
|---------|------------|
| **AWS** | Amazon Web Services, plataforma de computación en la nube de Amazon |
| **EC2** | Elastic Compute Cloud, servicio de máquinas virtuales en la nube |
| **AMI** | Amazon Machine Image, plantilla para crear instancias |
| **EBS** | Elastic Block Store, almacenamiento en bloques para EC2 |
| **S3** | Simple Storage Service, almacenamiento de objetos |
| **VPC** | Virtual Private Cloud, red virtual privada en AWS |
| **IAM** | Identity and Access Management, gestión de identidades y permisos |
| **Region** | Zona geográfica con datacenters de AWS |
| **AZ (Availability Zone)** | Centro de datos individual dentro de una región |
| **Security Group** | Firewall virtual para instancias y otros recursos |
| **Key Pair** | Par de claves SSH (pública/privada) para acceder a instancias |
| **CIDR** | Classless Inter-Domain Routing, método para definir rangos de IP |
| **SSH** | Secure Shell, protocolo para conexión segura a servidores |
| **On-Demand** | Modelo de pago por uso sin compromisos |
| **Reserved** | Modelo con descuento por compromiso a largo plazo |
| **Spot** | Instancias con descuento alto que pueden ser interrumpidas |
| **Free Tier** | Nivel gratuito para nuevos clientes de AWS |
| **ARN** | Amazon Resource Name, identificador único de recursos AWS |
| **IOPS** | Input/Output Operations Per Second, medida de rendimiento de almacenamiento |
| **Snapshot** | Backup point-in-time de un volumen EBS |
| **Bucket** | Contenedor de nivel superior en S3 |
| **Object** | Archivo almacenado en S3 |
| **IAM Role** | Permisos que puedes asignar a recursos o usuarios temporales |
| **MFA** | Multi-Factor Authentication, autenticación de múltiples factores |
| **CloudWatch** | Servicio de monitorización y logs de AWS |
| **RDS** | Relational Database Service, bases de datos gestionadas |
| **Lambda** | Servicio de computación sin servidor |
| **CLI** | Command Line Interface, interfaz de línea de comandos |
| **Console** | Interfaz web de gestión de AWS |
| **API** | Application Programming Interface, interfaz para programar servicios |

---

## Recursos adicionales

### Documentación oficial

- **AWS Documentation**: https://docs.aws.amazon.com
- **AWS Training**: https://aws.amazon.com/training/
- **AWS Free Tier**: https://aws.amazon.com/free/

### Labs prácticos

- **AWS Academy Learner Lab**: Labs proporcionados por tu instructor
- **AWS Workshop Studio**: Talleres prácticos guiados
- **QwikLabs**: Laboratorios prácticos (algunos gratuitos)

### Comunidades y ayuda

- **AWS re:Post**: Foro oficial de AWS (antes AWS Forums)
- **Stack Overflow**: Etiqueta `amazon-web-services`
- **r/aws**: Subreddit de AWS

---

*Este documento sirve como introducción a AWS para estudiantes sin conocimientos previos. La mejor forma de aprender es practicar, así que empieza a crear recursos en tu cuenta de AWS Academy.*
