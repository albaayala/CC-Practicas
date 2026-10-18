# Documentación hito 1

## Descripción del dominio


Para este proyecto se va a realizar una agenda de trabajo compartida entre el jefe y los trabajadores. En ella, el jefe crea, clasifica y asigna las tareas a sus trabajadores en un periodo de tiempo concreto. Además, el trabajador debe indicar cuando comenzó la tarea y cuando la finalizó. Todo ello, el sistema lo almacenará y podrá realizar estadísticas que ayuden al jefe a una mejora de la planificación.

Esta aplicación, ayuda a una empresa real, que ve ineficiente el reparto de tareas de forma verbal, además de que le gustaría digitalizarse. Asimismo, el jefe quiere saber qué tipo de tareas les cuesta más a los trabajadores o en cuales se suele producir más retraso, con el fin de realizar una mejor planificación.

Para facilitar el uso de usuarios del sistema, vamos a tener dos tipos:
- El administrador que cuyas funcionalidades están dirigidas al jefe de la empresa.
- El usuario que sus finalidades están dirigidas a los trabajadores.

### Casos de uso principales
| ID | Decripción | ACTOR |
| --- | --- | --- |
| CU-01 | Registrarse como empresa | Cualquiera |
| CU-02 | Iniciar sesión | Usuario registrado |
| CU-03 | Modificar los datos de mi usuario | Usuario registrado |
| CU-04 | Crear tipos de tareas | Administrador|
| CU-05 | Crear tareas |  Administrador |
| CU-06 | Modificar tareas | Administrador |
| CU-07 | Consultar mis tareas| Usuario |
| CU-08 | Marcar la tarea como iniciada | Usuario |
| CU-09 | Marcar la tarea como finalizada | Usuario |
| CU-08 | Ver estadísticas | Jefe |

### Justificación de porqué usar la nube
- La información sea acessible desde cualquier lugar y dispositivo.
- La carga es irregular, se concetrara en los horarios de trabajo.
- El pequeño negocio no puede o no quiern mantener sus propios servidores.

## Justificación del NIST
- **Autoservicio bajo demanda**: Una empresa nueva puede registrarse, crear su propio espcaico de trabajo y dar de alta a us trabajdores sin la intervención del proveedor. No hace falta instalar nada ni solicitar recursos a un administrador.
- **Agrupación de recusrsos**: Varias empresa comparten la misma infraestructura. Los datos se aislan lógiamente por un identificador de empresa prensente en todas las entidades y validado en cada petición. Los recursos se aisgna dinámicamente según la demanda, sin que el cliente conozca nada.
- **Rápida elasticidad**: La arquitectura de microservicios permite escalar cada servcio por separado, de esta forma, puede ser que el servicio de tareas tenga mayor necesidad de escaler a primera hora de la jornada, y en cambio la de estádisticas a final de la jornada.
- **Servicio medido**: EL uso de recusrso se monitoriza y se mide por empresa, lo que permite la facturación por uso ofereciendo transparecnia al proveedor y cliente.

# Mapeo de actores NIST
- **Consumidor**: La empresa cliente, tanto el jefe como sus trabajadores.
- **Proveedor**: El equipo de desarrollo de la aplicación  que operará sobre la infraestructura cloud (yo).
- **Intermediario**: Distribuidor que ofrezca el servicio a pequeños negocios (ficticio).
- **Auditor**: Quien nos evalúe la seguridad, privacidad y rendimiento (ficticio).
- **Operador**: Operador que conecte el cliente a la red para acceder al servicio.

  
