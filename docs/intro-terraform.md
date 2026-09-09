# Guía Completa de Terraform para Principiantes

## Tabla de Contenidos

1. [¿Qué es Terraform y por qué existe?](#qué-es-terraform-y-por-qué-existe)
2. [El problema que resuelve](#el-problema-que-resuelve)
3. [Conceptos fundamentales](#conceptos-fundamentales)
4. [El lenguaje HCL](#el-lenguaje-hcl)
5. [Providers: los drivers de terraform](#providers-los-drivers-de-terraform)
6. [Resources: los bloques de construcción](#resources-los-bloques-de-construcción)
7. [Variables: parametrizando configuraciones](#variables-parametrizando-configuraciones)
8. [Outputs: exponiendo información](#outputs-exponiendo-información)
9. [Data Sources: consultando recursos existentes](#data-sources-consultando-recursos-existentes)
10. [State: el corazón de Terraform](#state-el-corazón-de-terraform)
11. [El flujo de trabajo básico](#el-flujo-de-trabajo-básico)
12. [Primeros pasos prácticos](#primeros-pasos-prácticos)
13. [Estructura de un proyecto Terraform](#estructura-de-un-proyecto-terraform)
14. [Módulos: reutilizando código](#módulos-reutilizando-código)
15. [Workspaces: múltiples entornos](#workspaces-múltiples-entornos)
16. [Buenas prácticas](#buenas-prácticas)
17. [Errores comunes y cómo evitarlos](#errores-comunes-y-cómo-evitarlos)
18. [Glosario de términos](#glosario-de-términos)

---

## ¿Qué es Terraform y por qué existe?

Terraform es una herramienta de software creada por la empresa HashiCorp que permite definir, crear y gestionar infraestructura tecnológica mediante archivos de configuración declarativos. En términos sencillos: es un programa que lee unos archivos de texto donde tú describes cómo quieres que sea tu infraestructura (servidores, redes, bases de datos, almacenamiento, etc.), y se encarga de crear, modificar o destruir todos los componentes que hayas descrito para que la realidad coincida con lo que escribiste.

La palabra "declarativo" es importante aquí. En un lenguaje declarativo no le dices a la máquina "haz esto, luego haz esto otro, y después haz aquello". En su lugar, le describes el estado final que quieres alcanzar: "quiero un servidor con estas características, conectado a esta red, con este almacenamiento". Es Terraform quien decide qué pasos concretos necesita ejecutar para llegar desde la situación actual hasta ese estado deseado.

HashiCorp, la empresa detrás de Terraform, fue fundada en 2012 y se especializa en herramientas de infraestructura. Terraform se lanzó públicamente en 2014 y desde entonces se ha convertido en uno de los estándares de facto para la gestión de infraestructura como código, especialmente en entornos de nube pública como Amazon Web Services, Microsoft Azure o Google Cloud Platform.

La filosofía fundamental de Terraform se resume en una frase: "Infrastructure as Code". Tu infraestructura no vive en servidores físicos que alguien configura manualmente, ni en paneles de control web donde alguien hace clic en botones. Tu infraestructura está definida en archivos de texto, esos archivos viven en un repositorio Git como cualquier otro código, y esos archivos son la única fuente de verdad sobre cómo está configurado tu sistema.

---

## El problema que resuelve

Para entender realmente por qué existe Terraform, imagina el siguiente escenario sin él:

Un equipo de desarrollo necesita desplegar una aplicación web en la nube de Amazon Web Services. Antes de Terraform, el proceso sería aproximadamente este:

1. El responsable de operaciones accede al panel de control de AWS con su navegador
2. Busca la sección "EC2" (servidores virtuales) y hace clic en "Launch Instance"
3. Selecciona la imagen de máquina Amazon (AMI) adecuada, por ejemplo Ubuntu Server 22.04
4. Elige el tipo de instancia: t3.medium porque cree que será suficiente
5. Configura los detalles de la instancia: red, subred, protección contra terminación accidental
6. Añade almacenamiento: 20 GB de SSD gp3
7. Etiqueta la instancia con un nombre descriptivo
8. Configura el grupo de seguridad (firewall): permite tráfico por el puerto 22 (SSH) y 80 (HTTP)
9. Revisa todo y hace clic en "Launch"
10. Selecciona o crea un par de claves SSH para el acceso
11. Espera a que la instancia se inicialice
12. Anota la dirección IP pública que AWS le ha asignado
13. Se conecta por SSH al servidor
14. Ejecuta una serie de comandos para instalar Nginx, Node.js, las dependencias de la aplicación
15. Clona el repositorio de GitHub con el código de la aplicación
16. Instala PM2 para gestionar el proceso de Node
17. Configura Nginx como proxy inverso
18. Configura el dominio en Route 53 (DNS)
19. Obtiene un certificado SSL de Let's Encrypt con certbot
20. Configura el certificado en Nginx
21. Configura el firewall del sistema operativo
22. Configura el escalado automático, pero primero tiene que crear un "launch template"...
23. Crea un balanceador de carga, pero antes necesita crear un "target group"...
24. Configura las reglas del balanceador
25.... dos horas después, todo está funcionando

Ahora imagina que ese mismo equipo necesita crear tres entornos: desarrollo, staging y producción. Exactamente el mismo proceso, pero repetido tres veces. Probablemente con pequeñas diferencias entre unos y otros, porque nadie se acuerda de todos los pasos exactos. Y cuando algo falle en producción, nadie sabrá exactamente en qué difiere del entorno de staging, porque no hay documentación de qué se clickó exactamente.

Este enfoque manual tiene problemas fundamentales:

**Inconsistencia**: Cada vez que alguien configura algo a mano, hay riesgo de diferencias sutiles. Un puerto abierto en un servidor que se olvidó en otro. Una versión ligeramente diferente de una librería. Un ajuste de configuración que se hizo "temporalmente" y nunca se revirtió. Estas diferencias causan el famoso "funciona en mi máquina pero no en producción".

**Irrepetibilidad**: Si mañana necesitas exactamente la misma infraestructura en otra región o cuenta de AWS, tienes que recordar todos los pasos y repetirlos. Pero los humanos no somos buenos recordando detalles, así que inevitablemente algo será diferente.

**Sin historial**: Si algo se configuró mal y quieres saber cuándo y por qué se cambió, no hay forma de saberlo. El panel de control de AWS no guarda un log de todos los clics que hiciste hace tres meses.

**Escalado manual**: Si necesitas 50 servidores, tienes que repetir el proceso 50 veces. El error humano está prácticamente garantizado.

**Miedo al cambio**: Cuando la infraestructura es frágil y está mal documentada, nadie se atreve a tocarla por miedo a romper algo. Esto frena la innovación y hace que los entornos se deterioren con el tiempo.

Terraform resuelve todos estos problemas. Con Terraform, ese proceso completo de dos horas se convierte en un archivo de texto que se ejecuta en minutos, que produce exactamente el mismo resultado cada vez, que tiene un historial de cambios en Git, y que cualquier persona del equipo puede revisar, modificar y ejecutar.

---

## Conceptos fundamentales

Antes de profundizar en los detalles técnicos, es importante entender algunos conceptos que subyacen a cómo funciona Terraform.

### Declarativo vs Imperativo

Como se mencionó antes, Terraform usa un enfoque declarativo. Esto significa que tú describes el estado final deseado, no los pasos para llegar a él. La diferencia es similar a dar direcciones:

- **Enfoque imperativo** (lo que hace Ansible): "Gira a la derecha en la primera esquina, luego sigue recto dos kilómetros, después gira a la izquierda en el semáforo..."
- **Enfoque declarativo** (lo que hace Terraform): "Quiero estar en la Calle Mayor número 42"

Con el enfoque imperativo, si ya estás en la Calle Mayor número 42, seguirás las instrucciones y terminarás dando vueltas innecesariamente. Con el enfoque declarativo, el sistema detecta que ya estás donde quieres estar y no hace nada.

Esta diferencia tiene implicaciones importantes:

- **Idempotencia natural**: Ejecutar Terraform múltiples veces produce el mismo resultado que ejecutarlo una vez (asumiendo que el estado no ha cambiado externamente)
- **Menos errores**: No hay riesgo de ejecutar pasos en orden incorrecto o saltarse pasos
- **Más fácil de entender**: Solo necesitas describir qué quieres, no cómo lograrlo
- **Inteligencia integrada**: Terraform es lo suficientemente inteligente para calcular el camino más corto del estado actual al deseado

### Infrastructure as Code

Infrastructure as Code (IaC), o Infraestructura como Código en español, es el principio de gestionar y aprovisionar infraestructura mediante archivos de configuración y código, en lugar de procesos manuales. Esta no es solo una forma diferente de hacer las cosas, sino un cambio fundamental de paradigma.

Con IaC, tu infraestructura tiene estas características:

**Control de versiones**: Los archivos de configuración viven en Git. Cada cambio tiene un autor, una fecha y un mensaje de commit. Puedes crear ramas para experimentar, hacer pull requests para revisar cambios, y revertir cualquier cambio con un solo comando.

**Code review**: Antes de aplicar cambios a producción, alguien puede revisar el código en un pull request, igual que se revisa el código de la aplicación. Esto captura errores antes de que lleguen a producción.

**Reproducibilidad**: El mismo código produce el mismo resultado, indistintamente de quién lo ejecute o cuándo. Esto habilita entornos de desarrollo idénticos a producción, disaster recovery rápido, y capacidad de recrear entornos bajo demanda.

**Automación**: Los despliegues pueden automatizarse completamente. Un push a la rama main puede desencadenar automáticamente la creación o actualización de infraestructura en un pipeline de CI/CD.

**Documentación automática**: El código ES la documentación. No necesitas mantener documentos separados que inevitablemente se desactualizan. Si quieres saber cómo está configurado algo, miras el código.

### Estado de la infraestructura

En Terraform, el "estado" es un concepto central. El estado es un archivo JSON que Terraform utiliza para saber qué recursos existen actualmente en el mundo real. Sin el estado, Terraform no sabría la diferencia entre "crear un nuevo recurso" y "este recurso ya existe".

Cuando ejecutas `terraform apply`, Terraform:

1. Lee tus archivos de configuración (.tf)
2. Lee el archivo de estado actual (terraform.tfstate)
3. Compara el estado deseado (en los .tf) con el estado actual (en el .tfstate)
4. Calcula qué cambios necesita hacer para pasar del estado actual al deseado
5. Ejecuta esos cambios usando las APIs del proveedor de nube
6. Actualiza el archivo de estado con los nuevos recursos creados

El archivo de estado es crucial. Si lo pierdes, Terraform ya no sabe qué recursos fueron creados por él. Podrías terminar creando recursos duplicados o, peor aún, si intentas "destruir" todo, Terraform no sabrá qué destruir realmente.

Por esta razón, en entornos de producción el estado se guarda en un almacenamiento remoto (como un bucket S3 de AWS) con mecanismos de bloqueo para evitar que dos ejecuciones concurrentes se pisen unas a otras.

---

## El lenguaje HCL

Terraform utiliza HCL (HashiCorp Configuration Language) como lenguaje para sus archivos de configuración. HCL fue diseñado para ser legible por humanos pero procesable por máquinas, combinando una sintaxis clara con la capacidad de expresar estructuras de datos complejas.

### Archivos de configuración

Los archivos de configuración de Terraform tienen la extensión `.tf`. Puedes tener un solo archivo `main.tf` o dividir tu configuración en múltiples archivos para mayor organización. Terraform lee todos los archivos `.tf` en el directorio y los procesa como si fueran uno solo.

Por convención:

- `main.tf`: Recursos principales
- `variables.tf`: Definiciones de variables
- `outputs.tf`: Definiciones de outputs
- `providers.tf`: Configuración de providers
- `versions.tf`: Requisitos de versiones

Pero estas son solo convenciones. Terraform trata todos los archivos `.tf` de la misma manera.

### Sintaxis básica de HCL

HCL usa bloques para definir diferentes elementos de configuración. Cada bloque tiene un tipo, un nombre opcional entre paréntesis, y un cuerpo entre llaves que contiene argumentos.

```hcl
# Esto es un comentario

# Bloque de tipo "resource" llamado "ejemplo"
resource "tipo_recurso" "nombre_local" {
  # Argumentos
  argumento1 = "valor1"
  argumento2 = "valor2"
}
```

### Tipos de datos

HCL soporta varios tipos de datos:

**Strings**: Secuencias de caracteres entre comillas dobles.

```hcl
nombre = "mi-servidor"
region = "us-east-1"
```

**Números**: Pueden ser enteros o decimales.

```hcl
conteo = 3
memoria_gb = 4.5
```

**Booleanos**: true o false.

```hcl
habilitado = true
```

**Listas (arrays)**: Colecciones ordenadas de valores.

```hcl
# Lista de strings
zonas = ["us-east-1a", "us-east-1b", "us-east-1c"]

# Lista de números
puertos = [80, 443, 8080]
```

**Maps (objetos/diccionarios)**: Colecciones de pares clave-valor.

```hcl
# Map literal
configuracion = {
  entorno   = "produccion"
  rol       = "webserver"
  criticidad = "alta"
}
```

**Referencias a variables**: Puedes referenciar otras partes de tu configuración usando expresiones.

```hcl
nombre_completo = "${var.prefijo}-${var.nombre}"
```

### Interpolación de cadenas

Las cadenas en HCL pueden incluir expresiones interpoladas usando `${expresión}`. Esto permite concatenar valores, usar variables, y realizar operaciones.

```hcl
resource "aws_instance" "ejemplo" {
  tags = {
    Nombre = "Servidor-${var.entorno}"
    ID     = aws_instance.ejemplo.id  # Referencia al ID del recurso
  }
}
```

### Asignación condicional

Puedes usar condicionales dentro de interpolaciones:

```hcl
nombre_instancia = var.entorno == "produccion" ? "prod-server" : "dev-server"
```

### Expresiones aritméticas

Terraform soporta operaciones aritméticas básicas:

```hcl
total_ram = var.ram_por_servidor * var.numero_servidores
```

---

## Providers: los drivers de terraform

Los providers son plugins que permiten a Terraform interactuar con APIs externas. Cuando Terraform necesita crear un servidor en AWS, no habla directamente con AWS: usa el provider de AWS como intermediario. Cada provider es responsable de:

1. Entender la sintaxis de HCL para los recursos de ese provider
2. Traducir esa configuración a llamadas a la API del proveedor externo
3. Autenticarse con el servicio externo
4. Gestionar los recursos creados

### Providers principales

Aunque existen providers para cientos de servicios, los más usados son los de los grandes proveedores de nube:

**Amazon Web Services (AWS)**: El provider más popular, permite gestionar prácticamente cualquier servicio de AWS: EC2 (máquinas virtuales), S3 (almacenamiento), RDS (bases de datos), Lambda (funciones serverless), VPC (redes virtuales), y cientos más.

**Microsoft Azure**: Provider para los servicios de Microsoft Azure: Virtual Machines, Azure Storage, Azure SQL Database, Azure Kubernetes Service, etc.

**Google Cloud Platform (GCP)**: Provider para los servicios de Google Cloud: Compute Engine, Cloud Storage, Cloud SQL, GKE, etc.

**Kubernetes**: Provider especial que permite gestionar recursos dentro de un cluster de Kubernetes (pods, services, deployments, etc.).

**Docker**: Para gestionar contenedores y servicios Docker.

### Configuración de un provider

Para usar un provider, primero debes declararlo en tu configuración:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

Esto le dice a Terraform que vas a usar el provider de AWS y que todas las operaciones se realizarán en la región us-east-1.

### Autenticación

Los providers necesitan autenticarse con sus servicios. AWS, por ejemplo, puede obtener credenciales de varias fuentes (en orden de prioridad):

1. Credencialeshardcodeadas en la configuración del provider
2. Variables de entorno (AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY)
3. Credenciales almacenadas en ~/.aws/credentials (credenciales compartidas)
4. Roles de IAM (Identity and Access Management) para instancias EC2
5. AWS Single Sign-On (SSO)

**Nunca hardcodees credenciales en tus archivos .tf**. Usa variables de entorno o mecanismos de autenticación segura. Los archivos .tf se guardan en repositorios Git, y si alguien se descarga el repositorio, tendría tus credenciales.

La forma recomendada para desarrollo local es usar `aws configure` para guardar tus credenciales en ~/.aws/credentials, o configurar un profile con nombre.

```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "mi-profile"  # Nombre del profile en ~/.aws/credentials
}
```

O simplemente no especificar nada, y AWS usará el profile default.

### Locks y versiones de providers

Puedes especificar qué versión del provider quieres usar:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

Esto asegura que tu configuración funciona con versiones compatibles del provider. El símbolo `~>` significa "cualquier versión 5.x, pero no 6.0".

---

## Resources: los bloques de construcción

Los recursos son el elemento más importante en Terraform. Un recurso representa un componente de infraestructura que quieres crear y gestionar: una máquina virtual, una base de datos, un bucket de almacenamiento, una regla de firewall, un certificado SSL, una entrada DNS, etc.

### Sintaxis de un recurso

```hcl
resource "tipo_recurso" "nombre_local" {
  # Argumentos específicos del tipo de recurso
  argumento1 = "valor1"
  argumento2 = "valor2"
}
```

- **tipo_recurso**: El tipo de recurso que quieres crear, como `aws_instance`, `aws_s3_bucket`, `aws_vpc`, etc. El prefijo antes del guión bajo indica el provider (aws_, azurerm_, google_, etc.)
- **nombre_local**: Un nombre que tú eliges para identificar este recurso dentro de tu configuración. Este nombre es solo para Terraform, no tiene relación con el nombre del recurso en el proveedor de nube.
- **argumentos**: Parámetros que varían según el tipo de recurso. Algunos son obligatorios, otros opcionales.

### Ejemplo: creando una máquina virtual en AWS

```hcl
resource "aws_instance" "servidor_web" {
  # Imagen de máquina (AMI) - Ubuntu 22.04 LTS
  ami = "ami-0c55b159cbfafe1f0"

  # Tipo de instancia - define CPU y RAM
  instance_type = "t3.micro"

  # Nombre de la clave SSH para acceso
  key_name = "mi-clave-ssh"

  # Etiquetas para identificación y organización
  tags = {
    Name        = "ServidorWeb-Produccion"
    Environment = "produccion"
    Project     = "MiAplicacion"
    ManagedBy   = "terraform"
  }
}
```

### Dependencias implícitas entre recursos

Terraform deduce automáticamente las dependencias entre recursos. Por ejemplo:

```hcl
resource "aws_vpc" "mi_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subred" {
  vpc_id     = aws_vpc.mi_vpc.id  # Terraform sabe que esta subred depende de la VPC
  cidr_block = "10.0.1.0/24"
}
```

En este caso, Terraform sabe que la subred necesita que la VPC exista primero, así que siempre creará la VPC antes que la subred, incluso si en el archivo el recurso de la subred aparece antes.

### Dependencias explícitas

A veces necesitas indicar una dependencia que Terraform no puede deducir automáticamente:

```hcl
resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  # Dependencia explícita - Terraform esperará a que eks_cluster esté creado
  # incluso si no hay referencia directa
  depends_on = [
    aws_eks_cluster.example
  ]
}
```

### Recursos y sus argumentos

Cada tipo de recurso tiene sus propios argumentos. Los argumentos más comunes incluyen:

- **Identificadores**: Nombres, IDs, ARN (Amazon Resource Names)
- **Configuración de tamaño**: Tipo de instancia, capacidad de almacenamiento, etc.
- **Configuración de red**: VPC, subred, grupos de seguridad
- **Metadatos**: Etiquetas (tags) para organización y búsqueda
- **Configuración de acceso**: Claves SSH, políticas IAM, etc.

La documentación de cada recurso está en el Terraform Registry, donde puedes ver todos los argumentos disponibles, cuáles son obligatorios, y ejemplos de uso.

### El ciclo de vida de los recursos

Terraform gestiona el ciclo de vida completo de los recursos:

1. **Create (Crear)**: Cuando ejecutas terraform apply y detecta que un recurso no existe en el estado
2. **Update (Actualizar)**: Cuando existen diferencias entre la configuración y el estado actual. Algunos cambios pueden requerir destrucción y recreacion del recurso
3. **Delete (Eliminar)**: Cuando ejecutas terraform destroy o cuando eliminas el bloque de recurso de tu configuración

```hcl
resource "aws_instance" "ejemplo" {
  # Lifecycle block para controlar el comportamiento
  lifecycle {
    # Forzar recreacion del recurso en cada apply
    create_before_destroy = true

    # Prevenir destrucción accidental (útil para recursos críticos)
    prevent_destroy = true

    # Ignorar cambios externos a la configuración
    ignore_changes = [tags]
  }
}
```

### Tipos de recursos comunes en AWS

Para darte una idea de qué tipos de recursos existen, aquí hay algunos de los más usados:

| Tipo de recurso | Qué representa |
|----------------|----------------|
| `aws_vpc` | Una nube privada virtual |
| `aws_subnet` | Una subred dentro de una VPC |
| `aws_security_group` | Un firewall virtual |
| `aws_instance` | Una máquina virtual (servidor) |
| `aws_ebs_volume` | Un volumen de almacenamiento |
| `aws_s3_bucket` | Un bucket de almacenamiento de objetos |
| `aws_rds_instance` | Una base de datos gestionada |
| `aws_lb` | Un balanceador de carga |
| `aws_route53_record` | Un registro DNS |
| `aws_iam_role` | Un rol de identidad y acceso |
| `aws_sqs_queue` | Una cola de mensajes |
| `aws_sns_topic` | Un tema de notificaciones |

---

## Variables: parametrizando configuraciones

Las variables permiten que tu configuración de Terraform sea flexible y reutilizable. En lugar de hardcodear valores específicos, puedes definir parámetros que se establecen cuando se ejecuta Terraform.

### Definiendo variables

```hcl
variable "region" {
  description = "La región de AWS donde se crearán los recursos"
  type        = string
  default     = "us-east-1"
}
```

Cada variable tiene:

- **Nombre**: Cómo la referenciarás en tu código (var.region)
- **Description**: Explicación de para qué sirve (útil para otros y para terraform-docs)
- **Type**: El tipo de dato esperado (string, number, bool, list, map, etc.)
- **Default**: Un valor opcional por defecto

### Tipos de variables

```hcl
# String - texto
variable "nombre" {
  type    = string
  default = "mi-servidor"
}

# Number - números
variable "conteo" {
  type    = number
  default = 3
}

# Boolean - true o false
variable "habilitar_logs" {
  type    = bool
  default = true
}

# List - arrays ordenados
variable "zonas" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# Map - objetos clave-valor
variable "configuracion" {
  type = map(string)
  default = {
    entorno = "produccion"
    tier     = "application"
  }
}

# Set - colección sin duplicados
variable "puertos" {
  type    = set(number)
  default = [80, 443, 8080]
}

# Object - estructura compleja
variable "servidor" {
  type = object({
    cpu    = number
    ram    = number
    disco  = number
  })
  default = {
    cpu   = 2
    ram   = 8
    disco = 100
  }
}
```

### Validación de variables

Puedes añadir reglas de validación para asegurar que los valores son correctos:

```hcl
variable "entorno" {
  type    = string
  default = "desarrollo"

  validation {
    condition     = contains(["desarrollo", "staging", "produccion"], var.entorno)
    error_message = "El entorno debe ser: desarrollo, staging, o produccion."
  }
}

variable "tipo_instancia" {
  type    = string
  default = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.(micro|small|medium|large)$", var.tipo_instancia))
    error_message = "Tipo de instancia inválido. Usa formatos como t3.micro, t3.small, etc."
  }
}
```

### Usando variables en recursos

```hcl
variable "nombre_entorno" {
  type    = string
  default = "produccion"
}

variable "configuracion_servidor" {
  type = object({
    tipo_instancia = string
    cpu            = number
    ram_gb         = number
  })
  default = {
    tipo_instancia = "t3.micro"
    cpu            = 2
    ram_gb         = 1
  }
}

resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.configuracion_servidor.tipo_instancia

  tags = {
    Entorno = var.nombre_entorno
  }
}
```

### Pasando valores a Terraform

Hay varias formas de proporcionar valores para las variables:

**1. Archivo de variables por defecto (no recomendado para valores sensibles):**

```hcl
# terraform.tfvars (o .auto.tfvars)
region        = "us-west-2"
nombre_entorno = "produccion"
```

**2. En línea de comandos:**

```bash
terraform plan -var="region=us-west-2" -var="nombre_entorno=produccion"
```

**3. Variables de entorno (muy útil para CI/CD):**

```bash
export TF_VAR_region="us-west-2"
export TF_VAR_nombre_entorno="produccion"
terraform plan
```

**4. Archivos de variables específicos:**

```bash
terraform plan -var-file="env/produccion.tfvars"
```

---

## Outputs: exponiendo información

Los outputs son valores que Terraform calcula y muestra después de ejecutar un plan o apply. Son útiles para:

- Mostrar información importante al usuario (IPs, URLs, etc.)
- Compartir información entre módulos
- Facilitar la integración con otras herramientas

### Definiendo outputs

```hcl
output "ip_publica" {
  description = "Dirección IP pública del servidor"
  value       = aws_instance.servidor.public_ip
}
```

### Tipos de outputs

```hcl
# Output simple
output "id_servidor" {
  value = aws_instance.servidor.id
}

# Output con descripción sensible
output "password_bd" {
  description = "Contraseña de la base de datos (sensible)"
  value       = aws_db_instance.bd.password
  sensitive   = true
}

# Output estructurado (map u object)
output "informacion_servidor" {
  value = {
    id          = aws_instance.servidor.id
    ip_publica  = aws_instance.servidor.public_ip
    ip_privada  = aws_instance.servidor.private_ip
    dns         = aws_instance.servidor.public_dns
    zona        = aws_instance.servidor.availability_zone
  }
}

# Output de tipo list
output "subredes" {
  value = aws_subnet.privada[*].id
}
```

### Mostrando outputs

Después de un `terraform apply`, Terraform muestra los outputs automáticamente:

```
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

direccion_ip = "54.123.456.789"
id_servidor = "i-0abc123def456789"
```

Puedes ver los outputs en cualquier momento con:

```bash
terraform output
terraform output ip_publica
terraform output -json
```

### Usos prácticos de outputs

Los outputs son especialmente útiles para:

**Integración con Ansible**: Generar dinámicamente el archivo de inventario con las IPs de los servidores creados.

**Chain de módulos**: Pasar información de un módulo a otro sin acoplamiento directo.

**Pipeline de CI/CD**: Extraer valores para usar en siguientes pasos del pipeline.

```hcl
# Ejemplo: generar inventory de Ansible
output "ansible_inventory" {
  value = <<-EOT
    [servidores]
    ${aws_instance.servidor[0].public_ip}
    ${aws_instance.servidor[1].public_ip}
  EOT
}
```

---

## Data Sources: consultando recursos existentes

Los Data Sources permiten obtener información sobre recursos que YA existen, ya sea porque fueron creados fuera de Terraform, por otro equipo, o en otra cuenta de AWS. Es una forma de "consultar" datos sin crear nada.

### Usando un Data Source

```hcl
# Buscar la AMI más reciente de Ubuntu 22.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical (proveedor oficial de Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04 LTS-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Usar el resultado en un recurso
resource "aws_instance" "servidor" {
  ami = data.aws_ami.ubuntu.id
}
```

### Data Sources comunes

| Data Source | Qué hace |
|-------------|----------|
| `aws_ami` | Busca una imagen de máquina por criterios |
| `aws_vpc` | Obtiene información de una VPC existente |
| `aws_subnet` | Obtiene información de una subred |
| `aws_security_group` | Busca un grupo de seguridad |
| `aws_caller_identity` | Información de la identidad actual (cuenta, usuario, etc.) |
| `aws_region` | Información de la región actual |
| `aws_availability_zones` | Lista de zonas de disponibilidad |
| `aws_s3_bucket` | Obtiene información de un bucket existente |
| `terraform_remote_state` | Lee el state de otro proyecto Terraform |

### Ejemplo práctico: shared networking

Imagina que tienes una VPC de red compartida que fue creada por otro equipo:

```hcl
# Obtener la VPC compartida (sin crear una nueva)
data "aws_vpc" "compartida" {
  default = true  # Busca la VPC por defecto de la cuenta
}

# Obtener las subredes públicas de esa VPC
data "aws_subnet_ids" "publicas" {
  vpc_id = data.aws_vpc.compartida.id
  tags = {
    Type = "public"
  }
}

# Ahora podemos crear recursos en esa VPC existente
resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  subnet_id     = data.aws_subnet_ids.publicas.ids[0]
}
```

### Leyendo estado de otro workspace

El data source `terraform_remote_state` permite acceder al estado de otro proyecto Terraform:

```hcl
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "mi-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Ahora podemos usar las outputs del proyecto de networking
resource "aws_instance" "servidor" {
  # ...
  subnet_id = data.terraform_remote_state.networking.outputs.subnet_id
  vpc_id    = data.terraform_remote_state.networking.outputs.vpc_id
}
```

Esto es muy útil para separar proyectos: un proyecto para networking, otro para base de datos, otro para aplicaciones, donde cada uno consume las outputs de los anteriores.

---

## State: el corazón de Terraform

El estado (state) es quizás el concepto más importante y menos comprendido de Terraform. Sin el estado, Terraform no podría funcionar. Entender qué es el estado y cómo gestionarlo es crucial para usar Terraform de forma segura.

### Qué es el estado

El estado es un archivo JSON llamado `terraform.tfstate` que Terraform crea y mantiene. Este archivo contiene:

1. **Metadatos del estado**: Versión de Terraform, versión del state, serial, etc.
2. **Outputs**: Los valores de salida de tu configuración
3. **Recursos**: Un mapeo completo de cada recurso definido en tu configuración con el ID real del recurso en el proveedor de nube

```json
{
  "version": 4,
  "terraform_version": "1.5.0",
  "serial": 1,
  "lineage": "abc-123-def-456",
  "outputs": {
    "ip_publica": {
      "value": "54.123.456.789",
      "type": "string"
    }
  },
  "resources": [
    {
      "mode": "managed",
      "type": "aws_instance",
      "name": "servidor",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 1,
          "attributes": {
            "id": "i-0abc123def456789",
            "ami": "ami-0c55b159cbfafe1f0",
            "instance_type": "t3.micro",
            "public_ip": "54.123.456.789",
            "private_ip": "10.0.1.100",
            ...
          },
          "dependencies": ["aws_vpc.mi_vpc"]
        }
      ]
    }
  ]
}
```

### Por qué existe el estado

El estado sirve varios propósitos:

**Puente entre código y realidad**: Tus archivos .tf dicen "quiero un aws_instance llamado servidor". El estado dice "ese aws_instance tiene el ID i-0abc123def456789 y está en AWS con esta IP pública". Sin el estado, Terraform no sabría qué recurso de AWS corresponde a cada bloque de recurso en tu código.

**Rendimiento**: Consultar el estado es mucho más rápido que hacer llamadas API a AWS para cada recurso. Terraform usa el estado como cache de la realidad.

**Dependencias**: El estado registra las dependencias entre recursos para saber en qué orden crearlos.

### El problema del estado local

Por defecto, Terraform guarda el estado en un archivo local `terraform.tfstate` en el directorio del proyecto. Esto funciona bien para:

- Proyectos individuales
- Experimentación y aprendizaje
- Desarrollo local

Pero tiene problemas严重的 para entornos de equipo o producción:

**Sin compartir**: Cada persona del equipo tiene su propia copia del state. Si alguien ejecuta `terraform apply`, los demás no ven los cambios.

**Sin control de concurrencia**: Si dos personas ejecutan `terraform apply` al mismo tiempo, pueden corromper el estado.

**Riesgo de pérdida**: Si el archivo se borra o se corrompe, pierdes el tracking de tu infraestructura.

**Conflicts**: Cuando dos versiones del state divergen, resolver los conflictos es doloroso.

### Remote State (Estado Remoto)

La solución es usar un backend remoto que permita compartir el estado entre el equipo y prevenga accesos concurrentes.

**Backend S3 con DynamoDB para locking:**

```hcl
terraform {
  backend "s3" {
    bucket         = "empresa-terraform-state"      # Bucket S3 para guardar el state
    key            = "proyecto/entorno/terraform.tfstate"  # Path dentro del bucket
    region         = "us-east-1"
    encrypt        = true                            # Cifrado en reposo
    dynamodb_table = "terraform-locks"              # Tabla para bloquear cambios
  }
}
```

Esta configuración:

1. Guarda el estado en un bucket S3 (lo que permite versionado y auditoría)
2. Usa DynamoDB para implementar distributed locking
3. Si alguien está ejecutando `terraform apply`, otro que intente ejecutar simultáneamente recibirá un error indicando que el state está bloqueado
4. El estado se cifra automáticamente en S3

**Terraform Cloud como backend:**

```hcl
terraform {
  cloud {
    organization = "mi-empresa"
    workspaces {
      name = "mi-proyecto-produccion"
    }
  }
}
```

Terraform Cloud ofrece estado remoto, locking, un dashboard web para ver el historial, y ejecución remota de Terraform.

### State inspection

Puedes inspeccionar y manipular el estado con los comandos de state:

```bash
# Ver todos los recursos en el estado
terraform state list

# Ver detalles de un recurso específico
terraform state show aws_instance.servidor

# Renombrar un recurso (útil para refactoring)
terraform state mv aws_instance.servidor aws_instance.servidor_principal

# Eliminar un recurso del estado (no lo destruye en cloud)
terraform state rm aws_instance.servidor

# Importar un recurso existente al estado
terraform import aws_instance.existente i-0abc123def456789

# Ver el raw state en JSON
terraform state pull
```

### Remote state y workspaces

Los workspaces de Terraform (explicados más adelante) permiten tener múltiples estados separados usando el mismo código. Combinado con remote state:

```
Bucket S3: terraform-state/
├── proyecto/
│   ├── desarrollo/
│   │   └── terraform.tfstate
│   ├── staging/
│   │   └── terraform.tfstate
│   └── produccion/
│       └── terraform.tfstate
```

---

## El flujo de trabajo básico

Terraform tiene un flujo de trabajo claro y repetible que siempre sigues al trabajar con él. Entender este flujo es fundamental.

### Paso 1: Write (Escribir)

Empiezas creando o modificando tus archivos de configuración `.tf`. Aquí defines qué infraestructura necesitas:

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "MiServidor"
  }
}
```

### Paso 2: Init (Inicializar)

Antes de usar Terraform en un directorio nuevo o después de añadir nuevos providers o módulos, ejecutas `terraform init`:

```bash
terraform init
```

Qué hace internamente:

1. Lee los archivos de configuración
2. Identifica qué providers necesitas
3. Descarga los plugins de providers (se guardan en .terraform/providers/)
4. Inicializa el backend (local o remoto)
5. Prepara todo para poder ejecutar plan o apply

Solo necesitas ejecutar `init` una vez por proyecto o cuando cambias providers.

### Paso 3: Plan (Planificar)

Ejecutas `terraform plan` para ver qué cambios Terraform realizará:

```bash
terraform plan

# También puedes guardar el plan para revisarlo después
terraform plan -out=plan.tfplan
```

Terraform:

1. Lee tu configuración actual
2. Lee el estado actual (de terraform.tfstate o backend remoto)
3. Compara两者 (configuración vs estado)
4. Genera un plan mostrando qué creará, modificará o destruirá

La salida del plan es algo así:

```
Terraform will perform the following actions:

  # aws_instance.servidor will be created
  + resource "aws_instance" "servidor" {
      + ami                          = "ami-0c55b159cbfafe1f0"
      + arn                          = (known after apply)
      + associate_public_ip_address  = (known after apply)
      + availability_zone            = (known after apply)
      + id                           = (known after apply)
      + instance_type                = "t3.micro"
      + ip_address                   = (known after apply)
      + ...
      + tags                         = {
          + "Name" = "MiServidor"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

Revisa siempre el plan antes de aplicar. El plan te dice exactamente qué cambiará sin hacer realmente ningún cambio.

### Paso 4: Apply (Aplicar)

Cuando estás satisfecho con el plan, ejecutas `terraform apply` para aplicar los cambios:

```bash
# Versión interactiva (pregunta "yes" al final)
terraform apply

# Versión automática (para scripts o CI/CD)
terraform apply -auto-approve

# Aplicar un plan guardado previamente
terraform apply plan.tfplan
```

Terraform:

1. Ejecuta el plan (o genera uno nuevo si no le pasas un plan guardado)
2. Pide confirmación (a menos que uses -auto-approve)
3. Ejecuta los cambios usando las APIs del proveedor
4. Muestra el progreso de cada recurso
5. Actualiza el estado con los recursos creados

```
aws_instance.servidor: Creating...
aws_instance.servidor: Still creating... [10s elapsed]
aws_instance.servidor: Still creating... [20s elapsed]
aws_instance.servidor: Creation complete after 35s [id=i-0abc123def456789]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

### Paso 5: Destroy (Destruir)

Cuando ya no necesitas la infraestructura, puedes destruirla:

```bash
# Versión interactiva
terraform destroy

# Versión automática
terraform destroy -auto-approve
```

Terraform mostrará qué recursos destruirá y lo hará. **Sé muy cuidadoso con este comando en producción**.

### Visualización del flujo completo

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐            │
│   │  WRITE  │ ───▶ │   INIT  │ ───▶ │  PLAN   │            │
│   │  (.tf)  │      │         │      │         │            │
│   └─────────┘      └─────────┘      └────┬────┘            │
│                                          │                  │
│                                          ▼                  │
│                                    ┌─────────┐              │
│                                    │ REVIEW  │              │
│                                    │  (YES)  │              │
│                                    └────┬────┘              │
│                                          │                  │
│                                          ▼                  │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐            │
│   │ DESTROY │ ◀─── │ APPLY   │ ◀─── │         │            │
│   │         │      │         │      │         │            │
│   └─────────┘      └─────────┘      └─────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Validación y formateo

Antes de hacer plan o apply, es buena práctica:

```bash
# Validar sintaxis y semántica
terraform validate

# Formatear automáticamente el código para que sea consistente
terraform fmt

# Ambas cosas en un pipeline
terraform validate && terraform fmt
```

---

## Primeros pasos prácticos

### Instalación

**En macOS con Homebrew:**

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

**En Linux:**

```bash
# Descargar el binario
curl -fsSL https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip -o terraform.zip
unzip terraform.zip
sudo mv terraform /usr/local/bin/

# Verificar instalación
terraform version
```

**En Windows:**

Descarga el binario desde https://developer.hashicorp.com/terraform/downloads y añádelo al PATH.

### Credenciales de AWS

1. Crea una cuenta en AWS si no tienes una
2. En la consola de AWS, ve a IAM (Identity and Access Management)
3. Crea un usuario programmatic access
4. Asigna permisos (por ejemplo, AmazonEC2FullAccess para pruebas)
5. Guarda el Access Key ID y Secret Access Key

Configura las credenciales localmente:

```bash
# Opción 1: aws configure
aws configure

# Opción 2: Variables de entorno
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"
```

### Tu primer Terraform

Crea un directorio y un archivo:

```bash
mkdir mi-primer-terraform
cd mi-primer-terraform
```

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "mi_servidor" {
  ami           = "ami-0c55b159cbfafe1f0"  # Ubuntu 22.04 LTS en us-east-1
  instance_type = "t3.micro"

  tags = {
    Name        = "MiPrimerServidor"
    Environment = "desarrollo"
  }
}
```

Ahora ejecuta:

```bash
terraform init
terraform plan
terraform apply
```

Escribe `yes` cuando te pregunte, y en aproximadamente un minuto tendrás un servidor EC2 corriendo en AWS.

Para limpiar:

```bash
terraform destroy
```

---

## Estructura de un proyecto Terraform

Un proyecto Terraform bien organizado tiene una estructura clara:

```
mi-proyecto/
├── main.tf                 # Recursos principales
├── variables.tf            # Definiciones de variables
├── outputs.tf              # Definiciones de outputs
├── providers.tf            # Configuración de providers
├── versions.tf             # Requisitos de versiones
├── terraform.tfvars        # Valores de variables (NO subir a Git)
├── .gitignore              # Ignorar archivos sensibles
├── env/
│   ├── desarrollo.tfvars   # Variables para desarrollo
│   ├── staging.tfvars      # Variables para staging
│   └── produccion.tfvars   # Variables para producción
└── modules/                # Módulos reutilizables (opcional)
    └── servidor/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Ejemplo de variables.tf

```hcl
variable "region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "nombre_entorno" {
  description = "Nombre del entorno"
  type        = string
  validation {
    condition     = contains(["desarrollo", "staging", "produccion"], var.nombre_entorno)
    error_message = "El entorno debe ser desarrollo, staging o produccion."
  }
}

variable "configuracion_servidor" {
  description = "Configuración de los servidores"
  type = object({
    tipo_instancia = string
    ram_gb         = number
  })
  default = {
    tipo_instancia = "t3.micro"
    ram_gb         = 1
  }
}
```

### Ejemplo de outputs.tf

```hcl
output "id_servidor" {
  description = "ID de la instancia EC2"
  value       = aws_instance.mi_servidor.id
}

output "ip_publica" {
  description = "Dirección IP pública"
  value       = aws_instance.mi_servidor.public_ip
}

output "dns_publico" {
  description = "Nombre DNS público"
  value       = aws_instance.mi_servidor.public_dns
}
```

### Ejemplo de versions.tf

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Archivo .gitignore típico

```gitignore
# Terraform
.terraform/
.terraform.lock.hcl
*.tfstate
*.tfstate.*
crash.log
crash.*.log

# Override files
override.tf
override_*.tf
*_override.tf
*_override.tf.json

# Local .tfvars
*.tfvars
*.tfvars.json

# CLI configuration files
.terraformrc
terraform.rc
```

---

## Módulos: reutilizando código

Los módulos permiten organizar, reutilizar y parametrizar configuraciones de Terraform. Un módulo es simplemente un conjunto de archivos .tf que encapsulan recursos relacionados.

### Cuándo usar módulos

Imagina que necesitas crear 5 servidores web similares pero con pequeñas diferencias. Sin módulos, tendrías:

```hcl
# Opción sin módulos: repetir código
resource "aws_instance" "web1" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ... toda la config ...
}

resource "aws_instance" "web2" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ... casi la misma config ...
}
```

Esto es difícil de mantener. Si quieres cambiar algo común a todos, tienes que cambiarlo 5 veces.

Con un módulo:

```hcl
# main.tf
module "servidor_web" {
  source = "./modules/servidor"

  nombre        = "web1"
  entorno      = "produccion"
}

module "servidor_web" {
  source = "./modules/servidor"

  nombre        = "web2"
  entorno      = "produccion"
}
```

### Estructura de un módulo

```
modules/
└── servidor/
    ├── main.tf          # Los recursos del módulo
    ├── variables.tf     # Variables de entrada
    ├── outputs.tf       # Variables de salida
    └── README.md        # Documentación
```

**modules/servidor/main.tf:**

```hcl
resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.tipo_instancia

  tags = {
    Name = var.nombre
    Environment = var.entorno
  }
}

resource "aws_security_group" "servidor" {
  name = "${var.nombre}-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**modules/servidor/variables.tf:**

```hcl
variable "nombre" {
  description = "Nombre del servidor"
  type        = string
}

variable "entorno" {
  description = "Entorno (desarrollo, staging, produccion)"
  type        = string
}

variable "tipo_instancia" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}
```

**modules/servidor/outputs.tf:**

```hcl
output "id" {
  description = "ID de la instancia"
  value       = aws_instance.servidor.id
}

output "ip_publica" {
  description = "IP pública"
  value       = aws_instance.servidor.public_ip
}
```

### Módulos del Terraform Registry

No necesitas crear todos los módulos desde cero. El Terraform Registry tiene miles de módulos públicos maintained por HashiCorp, proveedores y la comunidad:

```hcl
# Usar módulo de VPC oficial de AWS
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "mi-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true
}
```

Este módulo de VPC te ahorra crear manualmente: una VPC, subredes públicas y privadas, gateways NAT, gateways de internet, tablas de enrutamiento, y más. Con ~15 líneas declaras lo que requeriría cientos de líneas de recursos individuales.

### Beneficios de usar módulos

1. **Reutilización**: Define una vez, usa muchas veces
2. **Abstracción**: Oculta detalles complejos detrás de una interfaz simple
3. **Mantenimiento**: Cambia en un lugar, aplica a todos los usos
4. **Organización**: Código más limpio y modular
5. **Testing**: Puedes probar el módulo aisladamente

---

## Workspaces: múltiples entornos

Los workspaces permiten tener múltiples estados diferentes para el mismo código. Es como tener múltiples copias de tu infraestructura sin duplicar los archivos .tf.

### Cuándo usar workspaces

Los workspaces son ideales para:

- Gestionar múltiples entornos (desarrollo, staging, producción) con el mismo código
- Branch de infraestructura para features
- Separation de state sin separation de código

### Usando workspaces

```bash
# Listar workspaces
terraform workspace list

# Crear workspace para staging
terraform workspace new staging

# Crear workspace para producción
terraform workspace new produccion

# Cambiar a un workspace
terraform workspace select staging

# Ver workspace actual
terraform workspace show
```

### Cómo funcionan los workspaces

Cada workspace tiene su propio archivo de estado:

```
Directorio del proyecto/
├── terraform.tfstate.d/
│   ├── desarrollo/
│   │   └── terraform.tfstate
│   ├── staging/
│   │   └── terraform.tfstate
│   └── produccion/
│       └── terraform.tfstate
```

El código es el mismo, pero cada workspace tiene su estado independiente. Así que cuando ejecutas `terraform apply` en el workspace de producción, solo se afectan los recursos del estado de producción.

### Variables específicas por workspace

Puedes usar el nombre del workspace en tus变量:

```hcl
locals {
  entorno = terraform.workspace
}

resource "aws_instance" "servidor" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = terraform.workspace == "produccion" ? "t3.medium" : "t3.micro"

  tags = {
    Environment = terraform.workspace
  }
}
```

### Alternativa: archivos de variables por entorno

Una alternativa común a los workspaces es usar archivos de variables separados:

```
env/
├── desarrollo.tfvars
├── staging.tfvars
└── produccion.tfvars
```

```bash
# Aplicar con variables de producción
terraform apply -var-file="env/produccion.tfvars"

# Plan con variables de staging
terraform plan -var-file="env/staging.tfvars"
```

Ambas aproximaciones son válidas. Los workspaces son convenientes cuando quieres cambiar rápidamente entre entornos. Los archivos de variables son mejores cuando los entornos tienen diferencias significativas que quieres controlar explícitamente.

### Consideraciones sobre workspaces remotos

Cuando usas remote state (S3), los estados de cada workspace se guardan en paths separados:

```
Bucket S3/
└── terraform-state/
    └── mi-proyecto/
        ├── desarrollo/
        │   └── terraform.tfstate
        └── produccion/
            └── terraform.tfstate
```

---

## Buenas prácticas

### Seguridad y gestión de secrets

**Nunca hardcodes secrets en archivos .tf:**

```hcl
# MAL - password en texto plano
resource "aws_db_instance" "bd" {
  password = "mi-password-secreto"  # ¡NO HACER ESTO!
}

# BIEN - usar variable con sensitive=true
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "bd" {
  password = var.db_password
}
```

**Fuentes seguras para secrets:**

- Variables de entorno (TF_VAR_*)
- AWS Secrets Manager o Parameter Store
- HashiCorp Vault
- Terraform Cloud / HCP Vault

```bash
# Pass secret via environment variable
export TF_VAR_db_password="mi-password-secreto"
terraform apply
```

### Control de versiones del código

**Usar control de versiones para toda la configuración:**

```bash
git init
git add .
git commit -m "feat: infraestructura inicial"
git push
```

**Reviews obligatorios:**

Nunca hagas `apply` directamente a producción. Usa pull requests para revisar cambios de infraestructura, igual que revisas cambios de código.

### Nomenclatura consistente

**Recursos:**

```hcl
# Usar prefijos claros
resource "aws_security_group" "app" {
  name = "${var.project}-${var.environment}-app"
}

resource "aws_instance" "web_server" {
  tags = {
    Name        = "${var.project}-web-${var.environment}"
    Project     = var.project
    Environment = var.environment
  }
}
```

**Variables:**

```hcl
variable "project_name" { }
variable "environment" { }
variable "instance_type" { }
variable "db_password" { sensitive = true }
```

### State management

**Siempre usar remote state en equipo:**

```hcl
terraform {
  backend "s3" {
    bucket         = "empresa-terraform-state"
    key            = "proyecto/${terraform.workspace}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**Backups automáticos:**

Con S3 como backend, habilita versionado para tener historial de estados:

```hcl
# El bucket S3 debe tener versioning habilitado
# Se puede hacer con otro apply de Terraform o manualmente
resource "aws_s3_bucket_versioning" "state" {
  bucket = "empresa-terraform-state"
  versioning_configuration {
    status = "Enabled"
  }
}
```

### Documentación

**Documentar módulos:**

Cada módulo debería tener un README.md:

```markdown
# Módulo: Servidor Web

Este módulo crea un servidor web EC2 con Nginx instalado.

## Uso

```hcl
module "web" {
  source = "./modules/servidor-web"

  nombre   = "mi-web"
  entorno  = "produccion"
}
```

## Inputs

| Variable | Descripción | Tipo | Default |
|----------|-------------|------|---------|
| nombre | Nombre del servidor | string | - |
| entorno | Entorno | string | desarrollo |

## Outputs

| Output | Descripción |
|--------|-------------|
| id | ID de la instancia |
| ip | IP pública |
```

### Control de cambios

**Usar terraform plan para revisar:**

Nunca hagas `apply` sin haber visto el plan. El plan es tu oportunidad de verificar que los cambios son los esperados.

**Target specific resources para cambios controlados:**

```bash
# Solo afecta un recurso específico
terraform plan -target=aws_instance.servidor_principal
terraform apply -target=aws_instance.servidor_principal
```

---

## Errores comunes y cómo evitarlos

### Error: "Circular dependency"

```
Error: Circular dependency between resources
```

**Causa**: Dos recursos dependen mutuamente el uno del otro.

**Solución**: Revisa las dependencias y usa `depends_on` para romper ciclos o restructure tu código.

### Error: "Provider not installed"

```
Error: Required plugin "provider.aws" not installed
```

**Causa**: No ejecutaste `terraform init` o el provider no está disponible.

**Solución**: Ejecuta `terraform init` para descargar los providers.

### Error: "State locked"

```
Error: Error acquiring the state lock
```

**Causa**: Otro proceso está ejecutando Terraform con el mismo state.

**Solución**: Espera a que termine el otro proceso. Si fue un crash, usa `terraform force-unlock`:

```bash
terraform force-unlock <lock-id>
```

### Error: "Resource already exists"

```
Error: Error creating resource: ResourceAlreadyExists
```

**Causa**: El recurso ya existe pero no está en tu state, o existe fuera de Terraform.

**Solución**: Importa el recurso existente al state:

```bash
terraform import aws_instance.existente i-0abc123def456789
```

### Error: "Diffencies detected"

Cuando ves cambios inesperados después de un `terraform plan`:

**Causa común 1**: Cambios externos a Terraform (otro equipo modificó algo en el panel de AWS).

**Solución**: Si los cambios fueron intencionales fuera de Terraform, actualiza tu código para reflejarlos y haz `terraform apply`. Si no fueron intencionales, identifica qué los causó.

**Causa común 2**: Diferencias en interpolación de strings (espacios extra, etc.).

**Solución**: Usa trimspace() para normalizar:

```hcl
tags = {
  Name = trimspace(var.nombre)
}
```

### Error: "Variables not set"

```
Error: Reference to undeclared variable
```

**Causa**: Usaste una variable que no está definida.

**Solución**: Define la variable en `variables.tf` o usa un valor por defecto.

### Error: "Destroy before create"

Cuando un recurso se destruye y se vuelve a crear en lugar de actualizarse:

**Causa**: Intentaste cambiar un atributo que no puede actualizarse in-place.

**Solución**: A veces esto es inevitable (por ejemplo, cambiar el tamaño de un volumen). Para ciertos recursos, usa `create_before_destroy` lifecycle:

```hcl
lifecycle {
  create_before_destroy = true
}
```

### Anti-patrones a evitar

1. **No usar remote state en producción**: Perderás el control de tu infraestructura
2. **No hacer apply sin plan previo**: Siempre revisa el plan
3. **No hardcodear valores**: Usa variables
4. **No ignorar los tags**: Los tags son esenciales para identificación y costes
5. **No compartir el state file localmente**: Usa remote backend
6. **No usar el workspace default para todo**: Usa workspaces o var-files para separar entornos

---

## Glosario de términos

| Término | Definición |
|---------|------------|
| **Apply** | Comando para aplicar los cambios definidos en los archivos .tf a la infraestructura real |
| **Backend** | Mecanismo de almacenamiento del archivo de estado (local, S3, Terraform Cloud, etc.) |
| **Provider** | Plugin que permite a Terraform interactuar con un servicio externo (AWS, Azure, GCP, etc.) |
| **Resource** | Componente de infraestructura definido en código (instancia, base de datos, red, etc.) |
| **Data Source** | Recurso existente leído de un provider externo, no gestionado por Terraform |
| **State** | Archivo JSON que mapea recursos en código con recursos reales en el provider |
| **HCL** | HashiCorp Configuration Language, el lenguaje declarativo de Terraform |
| **Plan** | Preview de los cambios que Terraform ejecutará |
| **Variable** | Parámetro de entrada que permite personalizar configuraciones |
| **Output** | Valor calculado y expuesto después de ejecutar Terraform |
| **Module** | Grupo de recursos encapsulado y reutilizable |
| **Workspace** | Estado aislado que permite gestionar múltiples entornos con el mismo código |
| **Import** | Acción de importar un recurso existente al state de Terraform |
| **Lifecycle** | Configuración que controla cómo se crean, actualizan y destruyen los recursos |
| **Dependency** | Relación entre recursos que indica cuál debe crearse primero |
| **Locking** | Mecanismo para prevenir ejecuciones concurrentes de Terraform |
| **Remote State** | Estado almacenado en un backend remoto (S3, Terraform Cloud) en lugar de localmente |
| **Drift** | Diferencia entre el estado real de la infraestructura y lo definido en el código |
| **Terraform Registry** | Repositorio público de providers y módulos de Terraform |
| **IaC** | Infrastructure as Code - práctica de gestionar infraestructura mediante código |

---

## Recursos adicionales

### Documentación oficial

- **Terraform Documentation**: https://developer.hashicorp.com/terraform/docs
- **Terraform Registry**: https://registry.terraform.io/
- **HashiCorp Learn**: https://developer.hashicorp.com/terraform/tutorials

### Libros

- "Terraform: Up and Running" por Yevgeniy Brikman - Excelente introducción práctica

### Comunidad

- **Terraform Discuss**: https://discuss.hashicorp.com/c/terraform-core/23
- **r/terraform** en Reddit
- **Stack Overflow**: Etiqueta `terraform`

---

*Este documento sirve como introducción a Terraform para estudiantes sin conocimientos previos. Profundiza en la documentación oficial y la práctica para dominar la herramienta.*
