# Mail-Tails

## Resumen

Mi proposito con este proyecto es crear un sistema automatizado para el envío masivo de correos electrónicos, construido con servicios serverless de AWS. Cargando un archivo .CSV con los destinatarios 

Mail Tails es un sistema automatizado para el envío masivo de correos electrónicos, construido con servicios serverless de AWS. Permite cargar archivos CSV con datos de destinatarios, personalizar los mensajes y enviar correos masivos mediante Amazon SES, utilizando AWS Lambda, Simple Storage Service, CloudWatch e IAM para garantizar eficiencia, seguridad y escalabilidad.

## Arquitectura

! [Arquitectura](/Mail-Tails/local/documentos/Arquitectura.png)

- Amazon EventBridge
- Amazon CloudWatch
- Amazon Simple Notification Service (SNS)
- Amazon Simple Storage Service (S3)
- AWS Lambda
- Amazon Simple Email Service (SES)
- AWS Identity and Access Management (IAM)