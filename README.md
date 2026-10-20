# Agenda interactiva entre la empresa y sus trabajdores
**Asignatura**: Cloud Computing.

**Autora**: Alba Ayala.

### ¿Qué se va a realizar?

Para esta práctica voy a realizar una agenda para que un administrador de una empresa cree tareas y se las asigne a sus trabajadores. Además de ello, el administrador podrá ver una serie de estádisictcas para que vea la evolución del trabajo.

### Enlaces a la entrega actual (Hito 1)
- [Ver documentación del hito 1](docs/hito1.md).
- [Ver documentación](https://github.com/albaayala/CC-Practicas/issues?q=is%3Aissue+state%3Aopen+label%3Auser-story).

### Gestión del proyecto

El repositorio sigue un flujo basado en *feature branches*:
- **`main`**: rama estable y protegida. No se puede subir código directamente a ella, ni borrarla, ni forzar cambios. Todo llega mediante Pull Request.
- **Ramas de trabajo**: se crea una por cada historia de usuario o cambio, a partir de `main`, con el formato `tipo/descripcion-corta`:

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feature/` | Nueva funcionalidad (una historia de usuario) | `feature/hu-06-crear-tareas` |
| `fix/` | Corrección de un error | `fix/validacion-solapes` |
| `docs/` | Documentación | `docs/readme-arquitectura` |
| `refactor/` | Mejora de código sin cambiar su comportamiento | `refactor/servicio-login` |


Los commits van a aseguir la siguiente convención:

|  Tipo | Cuándo se usa | Ejemplo |
|---|---|---|
| `feat` | Nueva funcionalidad | `feat: añadir endpoint de login` |
| `fix` | Corrección de un error | `fix: corregir validación de solapes de horario` |
| `docs` | Cambios en la documentación | `docs: actualizar diagrama de arquitectura` |
| `refactor` | Cambios internos sin alterar el comportamiento | `refactor: extraer validación de fechas` |
| `chore` | Configuración y mantenimiento | `chore: añadir .gitignore` |

El trabajo se organiza en:
- **Historias de usuario**: registradas como *Issues* con la etiqueta de *user-story*.
- **Milestones**: agrupa las historias de usuario por servicio.
- **Tablero**: con una vista de *board* por estado y otra vista agrupada en tablas por Milestone.







