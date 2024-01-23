# Práctica 4.1 - Configuración de Route 53 (DNS) en AWS

## Introducción
En este caso vamos a realizar una práctica similar a la anterior pero configurando el servidor DNS en un entorno de AWS.

Citando textualmente la [documentación de Amazon](https://docs.aws.amazon.com/es_es/Route53/latest/DeveloperGuide/Welcome.html):

!!!quote "Cita"
    Amazon Route 53 es un servicio web de sistema de nombres de dominio (DNS) escalable y de alta disponibilidad. Puede utilizar Route 53 para realizar tres funciones principales en cualquier combinación: registro de dominio, direccionamiento de DNS y comprobación de estado.
    

![](./img/route53-diagrama.png)


## Creación instancias EC2

Vamos a crear 3 instancias EC2:

1. Linux con Docker corriendo la web Juicy Shop
2. Linux que actuará como cliente para realizar las consultas DNS
3. Windows que actuará como cliente para realizar las consultas DNS

En primera instancia, debemos iniciar nuestro Learner Lab.


## Proceso en imágenes

![](./img/route53_1.png)

![](./img/route53_2.png)

![](./img/route53_3.png)

```bash title="Código"
#!/bin/bash 
yum update -y 
yum install -y docker 
service docker start 
systemctl enable docker.service
docker pull bkimminich/juice-shop 
docker run -d -p 80:3000 bkimminich/juice-shop
```

![](./img/route53_4.png)

![](./img/route53_5.png)

![](./img/route53_6.png)

![](./img/route53_7.png)

![](./img/route53_8.png)

![](./img/route53_9.png)

![](./img/route53_10.png)

![](./img/route53_11.png)

![](./img/route53_12.png)

![](./img/route53_13.png)

![](./img/route53_14.png)

![](./img/route53_15.png)

![](./img/route53_16.png)

![](./img/route53_17.png)

![](./img/route53_18.png)

![](./img/route53_19.png)

![](./img/route53_20.png)

![](./img/route53_22.png)

![](./img/route53_21.png)

![](./img/route53_23.png)

![](./img/route53_24.png)

![](./img/route53_25.png)

![](./img/route53_26.png)

![](./img/route53_27.png)

![](./img/route53_28.png)