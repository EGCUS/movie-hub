# Movie-hub - Diario del Equipo

- **Grupo**: G3
- **Nombre del grupo**: movie-hub
- **Tutores**: David Romero Organvidez y Jesús Moreno León
- **Curso Escolar**: 2025/2026
- **Asignatura**: Evolución y Gestión de la Configuración

---

## Índice

1. [Miembros del grupo](#1-miembros-del-grupo)
2. [Resumen de total de reuniones empleadas en el equipo](#2-resumen-de-total-de-reuniones-empleadas-en-el-equipo)
3. [Actas de acuerdos](#3-actas-de-acuerdos)
   - [ACTA 2025-01](#acta-2025-01)
   - [ACTA 2025-02](#acta-2025-02)
   - [ACTA 2025-03](#acta-2025-03)
   - [ACTA 2025-04](#acta-2025-04)
4. [Diario por participante](#diario-por-participante)
   - [Manuel Adame Mantecón](#manuel-adame-mantecón)
   - [Manuel Zoilo Buzón Muñoz](#manuel-zoilo-buzón-muñoz)
   - [Alejandro Carmona Reina](#alejandro-carmona-reina)
   - [Samuel Granado Oliva](#samuel-granado-oliva)
   - [Manuel Lavado Corredera](#manuel-lavado-corredera)
   - [Darío Román Jiménez](#darío-román-jiménez)
5. [Conclusión final](#conclusión-final)

---

## 1. Miembros del grupo

| **Nombre Completo**                | **UVUS** | **Email**                       |
|------------------------------------|----------|---------------------------------|
|Adame Mantecón, Manuel| GLL9619  | manadaman@alum.us.es      |
| Buzón Muñoz, Manuel Zoilo          |manbuzmun| manbuzmun@alum.us.es          |
| Carmona Reina, Alejandro           | CKR5791  | alecarrei1@alum.us.es        |
| Granado Oliva, Samuel              | VWN3805 | samgraoli@alum.us.es       |
| Lavado Corredera, Manuel            | manlavcor| manlavcor@alum.us.es      |
| Román Jiménez, Darío             | MBV3877| darromjim@alum.us.es     |

### Enlaces de interés:
- **Repositorio de código**: [https://github.com/EGCUS/movie-hub](https://github.com/Encocretados/uvlhub)  
- **Sistema desplegado**:
    - **Producción** (main): el sistema se encuentra desplegado en la web de despliegue render vista en las prácticas de la asignatura para el entorno de producción, al cual se puede acceder mediante el siguiente [enlace](https://movie-hub-lvra.onrender.com/).
    - **Desarrollo** (develop): el sistema se encuentra desplegado en la web de despliegue railway (parecida a render) para el entorno de producción, al cual se puede acceder mediante el siguiente [enlace](https://movie-hub-preview.up.railway.app/).
    - Además, para un mayor aislamiento, en el caso de que se necesitase o quisiese, el proyecto movie-hub tambien se puede desplegar tanto en el contenedor **docker** como en la máquina virtual **vagrant**, cuyas instrucciones se pueden encontrar en el archivo [readme del proyecto](https://github.com/EGCUS/movie-hub/blob/main/README.md).

---

## 2. Resumen de total de reuniones empleadas en el equipo

- **Total de reuniones (TR):** 4
- **Total de reuniones presenciales (TRP):** 2
- **Total de reuniones virtuales (TRV):** 2
- **Total de tiempo empleado en reuniones presenciales (TTRP):** 2h y 30 min
- **Total de tiempo empleado en reuniones virtuales (TTRV):** 4h

---

## 3. Actas de acuerdos

### ACTA 2025-01

**Asistentes:**

- Adame Mantecón, Manuel
- Buzón Muñoz, Manuel Zoilo
- Carmona Reina, Alejandro 
- Granado Oliva, Samuel
- Lavado Corredera, Manuel
- Román Jiménez, Darío

**Introducción:**

El equipo hizo una reunión presencial previa al entregable M1, la cual consistió en redactar los documentos acta fundacional y la política de ramas a seguir por el grupo.

**Acuerdos tomados:**
- **Acuerdo 2025-01-01: Acta fundacional - distinción de roles**.

   Se acordaron los distintos roles que se iban a establecer dentro del equipo para facilitar de esta manera la gestión del proyecto. Estos roles irían rotando a lo largo del transcurso del tiempo de desarrollo de movie-hub, y son los siguientes:

    - Jefe de proyecto.
    - Desarrollador.
    - Tester.

- **Acuerdo 2025-01-02: Acta fundacional - Compromisos del equipo**.

   Aquí el equipo expone cuáles son las acciones a las que se comprometen desde el inicio del proyecto.

- **Acuerdo 2025-01-03: Acta fundacional - Resolución de conflictos y penalizaciones**.
   En esta sección se muestra cómo el grupo va a lidiar con los conflictos, de tal manera que se impusieron una serie de supuestos problemas reales dentro de un proyecto y la manera de proceder ante estos problemas.

   Además, se exponen las distintas penalizaciones que se impondrán en función de la gravedad del conflicto. Las medidas a tomar van aumentando su dureza si persiste la dejadez o actitud perjudicial de cualquier miembro respecto al equipo completo. Las penalizaciones son
      - **Aviso verbal**: una forma de llamar la atención a un miembro del equipo para que corrija su actitud
      - **Amonestación**: aviso formal que se envía si se persiste en una actitud perjudicial para el proyecto incluso tras haber sido avisado, pudiendo derivar en consecuencias más graves.
      - **Aumento de trabajo**: si un miembro del equipo no cumple con las tareas correspondientes para el entregable, se penalizará con más carga de trabajo en el siguiente.
      - **Expulsión**: si el miembro del equipo no realiza la carga de trabajo extra impuesta por la sanción “aumento de trabajo”, se penalizará con la expulsión definitiva del equipo.


- **Acuerdo 2025-01-04: Política de gestión de ramas - Estructura**.
   
   El objetivo de este documento no es otro que establecer normas para la gestión de ramas dentro del proyecto, separando correctamente el código del desarrllador.

   Se establecieron dos ramas principales:
   - **main**: rama principal del proyecto, en ella solo se subirá el código cuando esté en condiciones de hacer una release.
   - **develop**: rama de producción, a ella se subirán todos los cambios que se vayan introduciendo mediante las ramas más pequeñas. Cuando el código esté listo para lanzar una release, se fusionará esta rama con main.

- **Acuerdo 2025-01-05: Política de gestión de ramas - tipos de ramas**.

   Se establecieron 4 tipos de ramas relacionadas con el contenido de los commits:
   - **feature**: una rama dedicada a añadir una nueva característica o funcionalidad.
   - **docs**: ramas en las que se añade o modifica la documentación del proyecto.
   - **fix**: ramas para arreglos de bugs.
   - **test**: ramas dedicadas a la implementación de pruebas.

- **Acuerdo 2025-01-06: Política de gestión de ramas - reglas relativas a las ramas**.

   Se establecieron 4 reglas:
   - **Nombres**: las ramas deben seguir esta estructura en sus nombres: `<tipo>/<nombre-con-guiones>`. Tiene especial importancia ya que de lo contrario puede que algunos flujos de trabajo no funcionen correctamente.

   - **Eliminación**: Como las ramas que no se vayan a utilizar más deben ser eliminadas, se definió un flujo de trabajo `.github/workflows/feature-branch` que, entre otras funciones, borra las ramas una vez se hace commit en ellas.

   - **Atomicidad**: No se deben realizar cambios que estén fuera de lo descrito en la issue para la que se haya creado la rama.

   - **Revisión**: Antes de fusionar una rama, es importante asegurarse de que el código del entorno local está actualizado y que los cambios de la rama no produzcan conflictos en el código.


### ACTA 2025-02

**Asistentes:**

- Carmona Reina, Alejandro 
- Granado Oliva, Samuel
- Román Jiménez, Darío

**Introducción:**

Algunos de los integrantes del equipo realizaron una reunión presencial previa al M1, se redactaron la política de gestión de commits y la política de gestión de issues. Además, se definieron los Work Items (WIs) a realizar por cada uno de los miembros del equipo acordados vía whatsapp debido a la falta de los compañeros no presentes en la reunión.

**Acuerdos tomados:**
- **Acuerdo 2025-02-01: Política de Commits**.

   Los mensajes de commit deben tener la siguiente forma: <tipo>: <nombre> El nombre debe describir brevemente lo que se ha hecho en el commit. Además, se definieron los siguientes tipos de commits:

    - **feat**: un commit que añade una nueva característica o funcionalidad.
    - **docs**: commits que se añaden o modifican la documentación del proyecto.
    - **fix**: commits para arreglos de bugs.
    - **test**: commits dedicados a la implementación de pruebas.

   Siguiendo el patrón de la gestión de ramas, tambien se redactaron reglas fundamentales para los commits:
    - **Commits atómicos**: cada commit solo debe incluir los cambios de su issue asociada.
    - **Ramas claras**: trabajar siempre en ramas dedicadas; prohibido modificar directamente develop o main.
    - **Revisión previa**: el autor debe asegurar que el código no rompe nada y pasa las pruebas antes de subirlo.

   Por último, se creó el workflow `.github/workflows/feature-branch.yml` el cual valida el formato y rechaza commits incorrectos.

- **Acuerdo 2025-02-02: Política de gestión de issues**.

   Las issues se gestionan en **ZenHub** y deben cumplir:
   - **Nombre breve** que resuma el propósito.
   - **Descripción** opcional si el nombre no es suficiente.
   - **Etiqueta** según el tipo: `feature`, `fix`, `test`, `docs`, `epic`.
   - **Milestone** asignada según el entregable.
   - **Épica** asociada si la tarea pertenece a un work item con épica.

   En zenhub, el responsable de la issue debe moverla según su estado:
   - **New issues:** creadas, sin asignar.
   - **To Do:** asignadas, aún sin iniciar.
   - **In Progress:** en desarrollo (recomendado 1 issue por desarrollador).
   - **Done:** finalizadas y fusionadas con `develop`.
   - **Closed:** tareas erróneas o duplicadas (no afecta al flujo).


- **Acuerdo 2025-02-03: Work Items**.

   Se han discutido los WI a implementar en el proyecto. Se ha acordado los siguientes WI:
    - **HIGH**:
        - **Differences between versions** *(Asignada a Buzón Muñoz, Manuel Zoilo)*: Este work item permite comparar distintas versiones de un dataset para identificar de forma clara qué ha cambiado entre ellas. Ofrece la posibilidad de ver archivos añadidos, eliminados o modificados, detectar cambios en los metadatos y visualizar las diferencias en formato diff para archivos de texto, facilitando así la evaluación del impacto de una actualización.
        - **Minor versioning (minor edition of datasets)** *(Asignada a Carmona Reina, Alejandro)*: Este work item permite realizar ediciones menores en un dataset sin modificar archivos ni contenido sustancial, siguiendo el modelo de Zenodo. Estas actualizaciones no generan un nuevo DOI, sino que actualizan el dataset existente, permitiendo editar metadatos básicos, gestionar autores y afiliaciones, y mantener un historial de cambios menores para garantizar la trazabilidad de las modificaciones.
    - **MEDIUM**:
        - **Trending datasets** *(Asignada a Román Jiménez, Darío)*: Este work item introduce una sección de datasets en tendencia para facilitar el descubrimiento de contenido popular en la plataforma. Muestra un ranking basado en visualizaciones o descargas recientes (semana o mes), incluyendo información clave como título, autor principal, comunidad y métricas de uso, ayudando a los usuarios a identificar rápidamente los datasets más relevantes.
        - **Exploration by communities** *(Asignada a Lavado Corredera, Manuel)*: Este work item permite a los visitantes filtrar los resultados de búsqueda por comunidad, facilitando la exploración de datasets asociados a un tema o institución concreta. Se añade un filtro de “Community” en la página de exploración, junto a los ya existentes, que limita los resultados a los datasets pertenecientes a la comunidad seleccionada. La interfaz muestra el nombre y el logotipo de la comunidad, mejorando la claridad y ayudando a los usuarios a encontrar contenido relevante y validado dentro de un contexto específico.
    - **LOW**:
        - **Rate limiting on login** *(Asignada a Granado Oliva, Samuel)*: Como sistema, se busca limitar el número de intentos de inicio de sesión fallidos para reforzar la seguridad de la plataforma y prevenir ataques de fuerza bruta. Esta funcionalidad permite detectar comportamientos sospechosos, aplicar bloqueos temporales o medidas de protección adicionales tras varios intentos fallidos y así proteger las cuentas de los usuarios y la integridad del sistema.
        - **Verification email** *(Asignada a Adame Mantecón, Manuel)*: Este work item establece el envío de un correo electrónico de verificación durante el proceso de registro, con el objetivo de validar la dirección de email proporcionada. Esta medida permite confirmar la autenticidad de las cuentas, reducir registros inválidos o fraudulentos y mejorar la seguridad y la calidad de los datos antes de habilitar el acceso completo a la plataforma.


### ACTA 2025-03

**Asistentes:**

- Carmona Reina, Alejandro 
- Granado Oliva, Samuel
- Román Jiménez, Darío

**Introducción:**

En esta reunión, elaborada de forma virtual, se decidió poner en marcha la refactorización de uvlhub para crear una clase base base dataset de la que las demás clases de tipos de datasets pudiesen heredar, todo esto previo a la entrega M2.

**Acuerdos tomados:**

- **Acuerdo 2025-03-01: Refactorización a base dataset inicial**  
  
  Desde este primer momento el equipo tuvo claro cuál iba a ser la idea principal, que no era otra que sacar todos los datos comunes que puedan tener distintos tipos de datasets a una clase base denominada **base dataset**, de tal manera que las clases de los distintos tipos de dataset como dataset (uvl, la del proyecto inicial) o moviedataset (creada por el equipo movie-hub) heredasen de esa clase base.

  Una vez hecho eso, tuvimos dos ideas para seguir:
   - Eliminar la clase dataset (uvl) y todas sus relaciones, de forma que solo quedase la clase moviedataset, ya que al fin y al cabo queríamos modificar la web para que se mostrasen únicamente datasets de películas, no datasets de uvl.
   - Dejar la clase dataset (uvl), ocupando cierto espacio en el código del proyecto, pero que no se mostrasen datos lógicamente de este tipo de dataset, solo datasets de películas.
  
  El equipo decidió como tarea ideal eliminar la clase dataset (uvl) y sus relaciones, ya que no se iba a usar, y de esta manera el código queda más limpio sin código inutilizado.

- **Acuerdo 2025-03-02: Creación de fakenodo**  
  
  Se analizó el codigo de zenodo del proyecto inicial para entender que había que hacer para la creación de fakenodo. De este análisis surgió la idea de que había que replicar con nuestros propios métodos los métodos de zenodo para conseguir hacer una API falsa que funcionase de forma parecida eliminando las restricciones que zenodo limitaba al proyecto base uvlhub. Además se propusieron pruebas para comprobar el correcto funcionamiento de dichas funciones.

### ACTA 2025-04

**Asistentes:**

- Carmona Reina, Alejandro 
- Granado Oliva, Samuel
- Román Jiménez, Darío

**Introducción:**

Se convocó una reunión virtual urgente de cara al entregable M2 debido a los problemas surgidos en la refactorización a base dataset definida en el primer acuerdo del anterior acta.

**Acuerdos tomados:**

- **Acuerdo 2025-04-01: Refactorización a base dataset final**

  Tras una primera refactorización, el equipo consiguió crear una clase base dataset y que las otras dos clases heredasen de ella.
  
  Sin embargo tuvo un problema bastante importante a la hora de intentar eliminar la clase dataset (uvl) con todas sus relaciones del código del proyecto, ya que daban múltiples fallos debido a las numerosas relaciones con prácticamente todas las clases que se encuentran en el proyecto.

  Debido a esto, el equipo decidió retroceder en esa decisión, tomando la segunda idea propuesta en el anterior acuerdo, que no era otra que dejar la clase dataset (uvl) ocupando cierto espacio en el código del proyecto, mostrándose únicamente datos de datasets de películas.
  
  De esta manera el equipo consiguió sortear el problema de relaciones entre clases y, aunque ocupaba cierto espacio, comprendió que era necesario dejarlo si no quería hacer una refactorización masiva del proyecto, algo que estaba fuera del alcance del equipo para la entrega M2.


# Diario por participante
 
## Manuel Adame Mantecón

### WI Asignado

En el proyecto, me he encargado del **WI Validacion de registro mediante correo electrónico**.

En resumen, he añadido una nueva pantalla tras el registro de un nuevo usuario en el sistema, en la que deberá añadir el código aleatorio de 6 dígitos que dicho usuario recibió en la dirección de correo electrónico especificada en el registro. Una vez introducido el código, se completará el registro y el usuario tendrá acceso al sistema.

La función send_email en `app/modules/auth/services.py` se encarga de enviar el correo electrónico según la plantilla `email_validation_form.html` en `app/modules/auth/templates/auth` y con el código aleatorio generado gracias a la función `generate_verification_code` también en `app/modules/auth/services.py`. Para ello, también ha sido creada la dirección de correo `moviehubegc@gmail.com`, desde la cual se enviarán automáticamente los correos cuando sea necesario.

En las primeras fases del desarrollo del WI, para probar el correcto funcionamiento del envío del correo, fue necesario probarlo registrando distintas direcciones de correo y observando su funcionamiento por consola para encontrar errores. Posteriormente, para poder gestionar los correos registrados y tener control sobre ello y los perfiles relacionados, fue conveniente crear una página para la gestión de usuarios. Para ello, se asignó el perfil con correo `user1@example.com` como administrador, y estando registrado con dicho perfil, se puede acceder a la página de gestión de usuarios a través de la barra lateral, página en la que también se pueden borrar y obtener datos de los distintos perfiles. Está página está creada en el módulo `app/modules/profile`.

### Pruebas Realizadas

En total: 3 pruebas unitarias para el modulo de auth en base al WI, 3 pruebas unitarias en el modulo de profile para la pantalla de gestión de usuarios, 1 prueba de carga en modulo auth.

Resumen de las pruebas creadas y ejecutadas (basado en los archivos de prueba presentes):

1) Pruebas unitarias (`app/modules/auth/tests/test_unit.py` líneas 81-94 / 130-174) — 3 pruebas:
    - `test_generate_verification_code`: Verifica que el código aleatorio de 6 dígitos se crea correctamente.
    - `test_email_validation_flow`: Verifica el correcto funcionamiento de la verificación mediante correo electrónico.
    - `test_email_validation_wrong_code`: Verifica que no se complete el registro si no se introduce el código correcto.
2) Pruebas unitarias (`app/modules/profile/tests/test_unit.py` líneas 41-115) - 3 pruebas:
    - `test_admin_requires_login`: Verifica que el admin esté registrado.
    - `test_admin_list_profiles_access_and_content`: Verifica que se lista correctamente los perfiles registrados.
    - `test_admin_delete_profile_flow`: Verifica el correcto funcionamiento de la eliminación de perfiles.
3) Pruebas Selenium
    - No se han realizado pruebas con seleniuk ya que tanto para el módulo de auth como el de profile se consideraba mala práctica de integración continua ya que era necesario el acceso al código aleatorio, que estaba incluido en el correo electrónico designado en el registro en cada caso.
4) Pruebas locust (`app/modules/auth/locustfile.py` líneas 58-91) - 1 prueba:
    - `EmailVerificationBehavior`: Verifica el correcto funcionamiento del WI con carga.

### Workflows Implementados

### Conclusión

Pese a ser un WI de dificultad baja, ha habido varios problemas debido a una mala implementación en primer momento. Sin embargo esas complicaciones se pudieron superar para terminar puliendo la funcionalidad de manera correcta.  No he tenido gran carga de trabajo en el proyecto y me ha costado addaptarme a la forma de trabajo de los integrantes del grupo, distinta a la mía, por lo que he trabajado bastante en solitario. Como forma de añadir funcionalidad extra y que ayudara al desarrollo del work item, para trastear en el proyecto se añadió la pantalla de gestión de usuarios por el administrador, lo cual ayudó a entender distintas funcionalidades del proyecto en campos distintos a los de mi work item original.

## Manuel Zoilo Buzón Muñoz

## Manuel Zoilo Buzón Muñoz

### WI Asignado

En el proyecto, me he encargado principalmente del **WI Differences between versions (comparación entre versiones de datasets)**.

Este work item tiene como objetivo permitir la comparación clara y estructurada entre distintas versiones de un mismo dataset de películas, facilitando al usuario la identificación de cambios introducidos entre versiones. Para ello, se implementó un sistema capaz de detectar y mostrar diferencias tanto a nivel de **metadatos** como de **contenido interno del dataset**, incluyendo películas añadidas, eliminadas o modificadas.

La funcionalidad permite seleccionar dos versiones de un mismo dataset y obtener un resultado estructurado que distingue entre:
- Cambios en metadatos.
- Películas añadidas.
- Películas eliminadas.
- Películas modificadas.

La lógica principal de comparación se implementó en el servicio `MovieService`, concretamente en el método `compare_version_ids()`, el cual carga ambas versiones del dataset y realiza una comparación exhaustiva de sus elementos, devolviendo un diccionario de diferencias que es utilizado tanto por vistas HTML como por endpoints específicos de comparación.

Esta funcionalidad resulta clave para el control de la evolución de los datasets y la trazabilidad de los cambios entre versiones.

### Pruebas Realizadas

En total: **pruebas unitarias del servicio de comparación, pruebas de interfaz con Selenium y escenarios de carga con Locust**, centradas específicamente en el WI de comparación de versiones.

Resumen de las pruebas creadas y ejecutadas:

#### 1) Pruebas unitarias (`app/modules/movie/tests/test_unit.py`) — 2 pruebas

- `test_compare_version_ids_detects_changes`  
  Verifica el correcto funcionamiento del método `compare_version_ids()`, comprobando:
  - Detección de cambios en metadatos entre versiones.
  - Identificación de películas añadidas entre dos versiones distintas.
  - Estructura correcta del resultado devuelto por el servicio.

- `test_compare_versions_page_renders`  
  Comprueba que la página de selección de versiones (`/moviedataset/<id>/versions`) se renderiza correctamente y muestra el mensaje esperado para seleccionar dos versiones a comparar.

#### 2) Pruebas Selenium (`app/modules/movie/tests/test_selenium.py`) — 2 pruebas

- `test_open_versions_selector`  
  Verifica que desde la vista de un dataset se puede acceder correctamente al selector de versiones.

- `test_compare_without_selection`  
  Comprueba el comportamiento de la interfaz cuando el usuario intenta comparar versiones sin haber seleccionado dos versiones válidas, validando que se muestra una alerta informativa.

Estas pruebas validan el flujo completo de usuario para la comparación de versiones desde la interfaz web.

#### 3) Pruebas de carga con Locust (`app/modules/movie/tests/locustfile.py`) — 2 escenarios

- `compare_versions_json`  
  Simula accesos concurrentes al endpoint de comparación de versiones en formato JSON (`/moviedataset/version/<v1>/compare/<v2>`).

- `compare_versions_view`  
  Simula accesos concurrentes a la vista HTML de comparación de versiones (`/moviedataset/version/<v1>/compare/<v2>/view`).

Estos escenarios permiten evaluar el comportamiento del sistema bajo carga en una funcionalidad clave del proyecto.

### Workflows Implementados

He participado en la automatización del proyecto mediante la creación y mantenimiento de workflows de CI/CD, destacando:

- **dockerhub_main.yml** (creador original): workflow encargado de construir y publicar automáticamente la imagen Docker del proyecto para la rama `main`.  
  Este workflow:
  - Se activa en cada push a `main`.
  - Construye la imagen Docker del proyecto.
  - Publica la imagen en Docker Hub con las etiquetas `latest` y el hash del commit.
  - Facilita el despliegue automático del sistema en entornos de producción.

Además, he colaborado en ajustes menores de workflows existentes para garantizar la correcta integración del WI dentro del pipeline de integración continua.

### Conclusión

Durante mi participación en el proyecto movie-hub, he contribuido principalmente a la implementación del sistema de **comparación entre versiones de datasets**, una funcionalidad clave para el control de cambios y la trazabilidad del contenido publicado en la plataforma.

El work item desarrollado permite identificar de forma clara y estructurada las diferencias entre dos versiones de un mismo dataset, tanto a nivel de metadatos como de contenido interno, ofreciendo soporte tanto en formato JSON como en vistas HTML. Las pruebas unitarias, de interfaz y de carga garantizan la estabilidad y fiabilidad de esta funcionalidad.

Estas aportaciones han reforzado la calidad técnica del proyecto y han establecido una base sólida para la evolución futura del sistema.


## Alejandro Carmona Reina
En el proyecto, me he encargado del **WI Minor versioning (minor edition of datasets) #84**.

Para realizar dicho WI, he implementado varias funciones en movieService que permiten editar los metadatos, autores y comunidades, de manera que los cambios queden registrados en un changelog sin que se produzca nuevo DOI. Se pueden consultar dichos cambios en la pantalla propia para changelog, donde de pueden los diferentes tipos de modificaciones y el tipo (editar, añadir o borrar). He precisado también de realizar un form para editar los metadatos del MovieDataset, donde además, he implementado una serie de validaciones para el ORCID y el autor que subió el dataset (este NO puede ser editado).

### Implementación de Upload y Fakenodo

He desarrollado la integración completa del sistema de upload con Fakenodo (mock de Zenodo), implementando dos flujos diferenciados:

1. **Upload como Draft**: Mediante `upload_draft_dataset()` en `MovieService`, el dataset se crea localmente y en Fakenodo con estado "draft", permitiendo al usuario revisar antes de publicar. El método crea el dataset, procesa los archivos JSON, genera el modelo de datos y sube los archivos a Fakenodo mediante `FakenodoAdapter`.

2. **Upload y Publish directo**: Con `upload_and_publish_dataset()`, el sistema ejecuta el flujo completo de creación y publicación inmediata, llamando internamente a `upload_draft_dataset()` seguido de `publish_fakenodo()` para asignar el DOI y cambiar el estado a "published".

He implementado `FakenodoAdapter` (`app/modules/fakenodo/adapter.py`) que actúa como capa de abstracción, permitiendo llamar directamente al servicio o a través de rutas HTTP según convenga. También corregí la ruta de subida de archivos a Fakenodo (`/fakenodo/upload/<int:fakenodo_id>`) para manejar correctamente el contenido binario y la validación de integridad mediante checksums MD5.

### Desarrollo de Interfaces

He contribuido significativamente en el desarrollo de las interfaces del módulo movie, implementando:

- **Carrusel 3D de películas** (`view_dataset.html`): Sistema interactivo con perspectiva 3D, posiciones calculadas dinámicamente, navegación por teclado y mouse, y animaciones suaves usando transiciones CSS3. El carrusel muestra hasta 5 películas simultáneamente con rotación Y y escalado según posición.

- **Pantallas dinámicas**: `list_datasets.html` con sistema de tarjetas responsivo, `manage_dataset.html` con opciones de gestión para propietarios, `upload_dataset.html` con validación de JSON en tiempo real y soporte multi-archivo, `edit_dataset.html` con gestión dinámica de autores y validaciones ORCID.

- **Changelog visual** (`changelog.html`): Timeline vertical con markers de colores según tipo de cambio (metadata: azul, autores: amarillo, comunidad: púrpura), diferenciación visual de elementos añadidos/eliminados con bordes verdes/rojos, y resumen estadístico de ediciones totales.

Además he contribuido también en `view_movie.html`
### Pruebas Realizadas

He desarrollado un conjunto completo de pruebas para garantizar la calidad del código:

1) **Pruebas unitarias** (`app/modules/movie/tests/test_unit.py`) — 15+ pruebas:
   - Tests de rutas GET/POST para la un gran porcentaje de los endpoints del módulo movie
   - Verificación de redirecciones, autenticación y permisos
   - Tests específicos de changelog: `test_view_changelog()`, `test_api_changelog()`
   - Tests de edición: `test_edit_dataset_metadata_get()`, `test_edit_dataset_metadata_post()`, `test_edit_dataset_metadata_forbidden()`
   - Tests de upload: `test_upload_dataset_as_draft()`, `test_upload_dataset_and_publish()`, `test_upload_dataset_validation_error()`
   - Tests de publicación: `test_publish_dataset_success()`, `test_publish_dataset_forbidden()`, `test_publish_dataset_no_fakenodo()`

2) **Pruebas Selenium** (`app/modules/movie/tests/test_selenium_upload_and_edit_metadata.py`) — 1 test completo:
   - `test_upload_draft_and_publish_plus_direct_publish()`: Test end-to-end que verifica login, upload como draft, publicación del draft, upload y publish directo, doble edición de metadata y verificación del changelog completo

3) **Pruebas Locust** (`app/modules/movie/tests/locustfile.py`) — 10+ escenarios:
   - `upload_dataset_as_draft()`: Simula subida de datasets con action=draft
   - `upload_and_publish_directly()`: Test de publicación directa con action=publish
   - `publish_existing_draft()`: Publicación de drafts existentes
   - `upload_multiple_files()`: Test con múltiples archivos JSON
   - `compare_versions_json()`, `compare_versions_view()`: Tests de comparación de versiones
   - `edit_dataset_metadata()`, `view_changelog()`: Tests de edición y changelog

### Workflows Implementados

He contribuido en la configuración de workflows de CI/CD:

1) feature-branch.yml (creador): Workflow principal para ramas temporales que valida mensajes de commit según convención (feat/fix/test/docs) y orquesta la ejecución paralela de otros workflows. Implementa verificación de formato de commit con regex y manejo de errores con mensajes descriptivos.

2) release.yml (pequeña contribución): Workflow de releases automáticos usando semantic-release. Se activa en push a main con commits de tipo "chore(release)", genera versiones semánticas según commits convencionales, crea changelog automático y publica releases en GitHub con notas generadas.

### Conclusión

Durante mi participación en el proyecto movie-hub, he contribuido principalmente en cuatro áreas clave: versionado menor de datasets, integración con Fakenodo, desarrollo de interfaces y testing exhaustivo.

El work item de minor versioning implementado permite la evolución controlada de datasets sin proliferación de DOIs, manteniendo trazabilidad completa mediante un sistema de changelog visual. La integración con Fakenodo establece un flujo completo de publicación con dos modalidades (draft y publish directo), facilitando la gestión del ciclo de vida de los datasets.

El desarrollo de interfaces con componentes dinámicos como el carrusel 3D de películas y las pantallas de edición con validaciones en tiempo real mejora significativamente la experiencia de usuario. Junto a mis compañeros Darío Román Jiménez y Samuel Granado Oliva, participé en la refactorización de la clase **BaseDataset** que permitió la extensibilidad del sistema.

Finalmente, la implementación de pruebas unitarias, Selenium y Locust, junto con los workflows de CI/CD, garantiza la estabilidad del sistema y automatiza procesos críticos de testing y despliegue. Estas contribuciones han fortalecido tanto la funcionalidad como la calidad técnica del proyecto, estableciendo bases sólidas para su evolución futura.

## Samuel Granado Oliva

### WI Asignado

En el proyecto, me he encargado del **WI Limitar los intentos fallidos de inicio de sesión para evitar ataques de fuerza bruta**.

Como resumen, he implementado un sistema de rate limiting en el módulo de autenticación que limita los intentos fallidos de login a un máximo de 3 por sesión. Después del tercer intento fallido, el usuario queda bloqueado por un tiempo que aumenta exponencialmente (30 segundos inicialmente, duplicándose en cada intento adicional). El contador de intentos se resetea automáticamente cuando el usuario logra autenticarse correctamente.

La implementación se basa en el almacenamiento de estado en la sesión de Flask (`session["login_attempts"]` y `session["blocked_until"]`), lo que permite un control eficiente sin necesidad de persistencia en base de datos. El servicio `AuthenticationService` en `app/modules/auth/services.py` maneja toda la lógica, con constantes configurables como `MAX_ATTEMPTS = 3` y `BASE_BLOCK_TIME = 30`.

### Pruebas Realizadas

En total: 2 pruebas unitarias específicas para el rate limiting de login, 1 prueba de interfaz para el flujo de login con rate limiting, 4 pruebas de interfaz para funcionalidades del módulo movie, y arreglos en pruebas unitarias del módulo movie.

Resumen de las pruebas creadas y ejecutadas (basado en los archivos de prueba presentes):

1) Pruebas unitarias (`app/modules/auth/tests/test_unit.py` líneas 96-128) — 2 pruebas
    - `test_login_success_resets_attempts`: Verifica que un login exitoso resetea el contador de intentos fallidos.
    - `test_login_block_after_max_attempts`: Verifica que después de 3 intentos fallidos, el usuario queda bloqueado y recibe un mensaje de "Too many requests".

2) Pruebas Selenium (`app/modules/auth/tests/test_selenium.py` líneas 52-78) — 1 prueba
    - `TestInvalidcredentials1attempt.test_invalid_credentials_shows_right_texts`: Simula intentos fallidos de login desde la interfaz web y verifica que se muestran los mensajes correctos ("Invalid credentials. X attempts remaining") y el bloqueo final ("Too many requests. Please wait 30 seconds").

3) Pruebas Selenium (`app/modules/movie/tests/test_selenium.py` — todo el archivo) — 4 pruebas
    - `test_explore_datasets_home`: Verifica que la página de exploración de datasets es accesible y contiene referencias a "Movie".
    - `test_view_movie_collection`: Verifica que se puede ver la colección de películas de un dataset (carrusel).
    - (Otras pruebas adicionales para navegación y funcionalidad del módulo movie).

4) Arreglos en pruebas unitarias del módulo movie (`app/modules/movie/tests/test_unit.py`)
    - Se arreglaron pruebas relacionadas con las rutas y servicios del módulo movie, incluyendo verificación de redirecciones, autenticación requerida, llamadas a servicios mockeados, y respuestas HTTP correctas para endpoints como `/moviedataset/list`, `/moviedataset/my-datasets`, y otras funcionalidades del módulo.

### Workflows Implementados

Se implementaron y configuraron múltiples workflows de GitHub Actions para automatizar el proceso de CI/CD, testing, análisis de calidad y despliegue. Todos los workflows están ubicados en `.github/workflows/` y se activan en diferentes eventos (push, workflow_call, etc.).

1) **codacy.yml** (creado): Workflow para análisis de cobertura de código con Codacy. Se activa en push a main o por llamada desde otros workflows. Configura una base de datos MySQL temporal, instala dependencias, ejecuta pruebas con pytest (excluyendo Selenium), genera reporte de cobertura XML y lo sube automáticamente a Codacy para análisis de calidad y métricas.

2) **dockerhub_main.yml** (modificado): En colaboración con el compañero Manuel Zoilo Buzón Muñoz que lo creó originalmente. Workflow para construcción y publicación de imágenes Docker en Docker Hub para la rama main. Se activa en push a main o manualmente. Construye imágenes con tags latest y commit hash, las publica en moviehubuser/movie-hub, y limpia automáticamente imágenes antiguas para optimizar espacio.

3) **dockerhub_develop.yml** (creado): Similar al anterior pero para rama develop. Se activa por workflow_call. Publica imágenes en moviehubuser/movie-hub-preview con credenciales de desarrollo, incluyendo limpieza de imágenes antiguas.

4) **feature-branch.yml** (modificado): Workflow principal para ramas temporales. Valida mensajes de commit según convención (feat/fix/test/docs), y llama a otros workflows (codacy, tests, dockerhub) para ejecutar pruebas, análisis de calidad y publicación de imágenes en paralelo. Yo me encargué de añadir las llamadas a otros workflows, este fue creado originalmente por el compañero Alejandro Carmona Reina.

5) **railway.yml** (creado): Workflow de despliegue a Railway para rama develop. Configura Python 3.12, instala dependencias, actualiza base de datos y ejecuta seeders, luego despliega automáticamente a Railway usando la CLI.

6) **release.yml** (creado): Workflow de releases automáticos usando semantic-release. Se activa en push a main con commits de tipo "chore(release)". Genera versiones semánticas, changelog y releases en GitHub basándose en commits convencionales.

7) **tests.yml** (creado): Workflow dedicado a ejecución de pruebas unitarias. Se activa en push a main o por workflow_call. Configura MySQL temporal, instala dependencias y ejecuta pytest en todos los módulos (excluyendo pruebas Selenium) con configuración de testing.

### Conclusión

Durante mi participación en el proyecto movie-hub, he contribuido principalmente en tres áreas clave: seguridad de autenticación, refactorizaciones y automatización de CI/CD. El work item de rate limiting de login implementado añade una capa esencial de protección contra ataques de fuerza bruta, mejorando la robustez del sistema sin comprometer la experiencia de usuario. Junto a mis compañeros Darío Román Jiménez y Alejandro Carmona Reina refactorizamos la clase **BaseDataset** que permitió la convivencia de distintos tipos de datasets en el sistema. Finalmente, los workflows de GitHub Actions automatizan procesos críticos como testing, análisis de calidad, construcción de imágenes Docker y despliegues, reduciendo errores manuales y acelerando el ciclo de desarrollo. Estas contribuciones han fortalecido la infraestructura técnica del proyecto, facilitando un desarrollo más seguro, eficiente y escalable.


## Manuel Lavado Corredera

### WI Asignado

### Pruebas Realizadas

### Workflows Implementados

### Conclusión


## Darío Román Jiménez

### WI Asignado

Durante el período actual, me he encargado del **WI Trending datasets #100**.

Como resumen, he conseguido que se muestre en la pantalla principal "home" datasets de películas en tendencia, es decir, los 3 datasets de películas que más se han descargado el último mes, **sin tener en cuenta descargas de borradores**, incluyendo algunas propiedades como su título, su autor principal y el número de descargas que dicho dataset posee, además de dar la posibilidad de que el usuario vea sus detalles y/o descargue el dataset.

Si no hubiese aún ningun dataset descargado el último mes, el banner se sigue mostrando con el siguiente texto informativo: *No datasets have been downloaded this month yet. Be the first to download a dataset!*

### Pruebas Realizadas

En total: 26 pruebas unitarias y 6 escenarios de Locust 1 prueba Selenium.

Resumen de las pruebas creadas y ejecutadas para el WI "Trending datasets" (basado en los archivos de prueba presentes): `test_selenium.py`, `test_unit.py` y `locustfile.py`.

1) Pruebas unitarias (`app/modules/dataset/tests/test_unit.py`) — 17 pruebas

    - Objetivo: comprobar contratos y comportamientos de la capa de repositorio y del servicio de descargas, y validar la extracción/normalización de metadatos (autor, objeto dataset, conteos).

    - Tests del repositorio (`DSDownloadRecordRepository.top_downloaded_datasets_last_month`) — 5 pruebas:
       - `test_top_downloaded_datasets_returns_list`: verifica que el método devuelve una lista.
       - `test_top_downloaded_datasets_returns_tuples_with_dataset_id_and_count`: comprueba que cada elemento es una tupla (dataset_id, count) y que los valores coinciden con lo esperado.
       - `test_top_downloaded_datasets_respects_limit_parameter`: asegura que el parámetro `limit` se respeta y se pasa correctamente al método.
       - `test_top_downloaded_datasets_filters_by_last_month`: valida la lógica de filtrado por fecha (último mes) cuando no hay descargas en el periodo (mocked).
       - `test_top_downloaded_datasets_empty_results`: confirma que el método devuelve lista vacía si no existen descargas.

    - Tests del servicio (`DSDownloadRecordService.top_downloaded_datasets_last_month`) — 12 pruebas:
       - `test_service_returns_list_of_dicts`: asegura que el servicio transforma la salida del repositorio en una lista de diccionarios.
       - `test_service_returns_dict_with_required_keys`: verifica que cada diccionario contiene las claves `dataset`, `download_count` y `author`.
       - `test_service_includes_download_count_correctly`: comprueba que los `download_count` en los dicts coinciden con los valores devueltos por el repositorio.
       - `test_service_extracts_author_from_dataset`: extrae el nombre del primer autor cuando el dataset tiene metadata y autores definidos.
       - `test_service_handles_dataset_without_metadata`: si `ds_meta_data` es `None`, el campo `author` se normaliza a cadena vacía.
       - `test_service_handles_dataset_without_authors`: si `ds_meta_data.authors` es `None`, `author` es cadena vacía.
       - `test_service_handles_empty_authors_list`: si la lista de autores está vacía, `author` es cadena vacía.
       - `test_service_includes_dataset_object`: verifica que el objeto `MovieDataset` (mock) se incluye en el resultado y mantiene atributos como `id`.
       - `test_service_respects_limit_parameter`: asegura que el servicio llama al repositorio con el `limit` correcto (assert sobre el mock).
       - `test_service_returns_only_limited_results_when_more_exist`: prueba que, aunque existan más datasets, el servicio devuelve sólo la cantidad limitada (ej. 3) basada en la respuesta del repositorio.
       - `test_service_returns_empty_list_when_no_downloads`: confirma que el servicio devuelve `[]` cuando el repositorio no reporta descargas.
       - `test_service_handles_multiple_datasets_with_authors`: valida que múltiples datasets con distintos autores se procesan y que los `author` devueltos coinciden con cada dataset.

    - Técnica: los tests usan `unittest.mock` para stubear el método del repositorio y `MovieDataset.query.get`, haciendo las pruebas rápidas y aisladas de SQLAlchemy.

2) Pruebas de carga / integración ligera con Locust (`app/modules/dataset/tests/locustfile.py`) — 5 escenarios

    - Objetivo: validar comportamiento bajo carga y la dinámica del ranking "trending" tras descargas repetidas.
    - Escenarios contemplados:
       - `DatasetBehavior` / `DatasetUser`: accesos a upload y páginas de dataset.
       - `TrendingDatasetsBehavior` / `TrendingDatasetsUser`: navegación y comprobación de trending, accesos y descargas.
       - `CombinedBehavior` / `CombinedUser`: mezcla de navegación general y acciones sobre trending.
       - `RankingUpdateBehavior` / `RankingUpdateUser`: descarga repetida y verificación de cambios en el ranking.
       - `HighVolumeDownloadBehavior` / `HighVolumeDownloadUser`: simulación de alto volumen de descargas para verificar consistencia.

3) Pruebas Selenium (`app/modules/public/tests/test_selenium.py`) — 1 prueba end-to-end

    - Objetivo: recorrido end-to-end de la interfaz para comprobar navegación, login, descargas y acciones de usuario.
    - Pasos clave automatizados por el script:
       - Acceder a la página principal (`/`) y realizar descargas desde enlaces "Download (... KB)".
       - Abrir/cerrar la barra lateral y navegar entre Home y otras vistas.
       - Login como `user1@example.com` y uso de botones de la lista de datasets (ver/descargar/acciones relacionadas).
       - Verificación básica de que modales y redirecciones funcionan correctamente.

Además, he realizado pruebas unitarias y locust para la clase MovieDataset, la cual deriva de la clase base BaseDataset:

1) Pruebas unitarias (`app/modules/movie/tests/test_unit.py`) — 9 pruebas

   - Objetivo: verificar las rutas y comportamientos clave de `moviedataset` y `movie` (listados, vistas, descargas y comparación de versiones).
   - Tests principales (resumen):
     - `test_index_redirects_to_list`: comprueba redirección de `/moviedataset` a `/moviedataset/list`.
     - `test_list_datasets`: valida que el listado muestra los títulos de los datasets.
     - `test_my_datasets_requires_login`: asegura que `/moviedataset/my-datasets` funciona con usuario autenticado.
     - `test_view_dataset`: renderiza detalle de dataset y verifica que se setea la cookie de visualización.
     - `test_view_movie`: muestra la página de una película y sus datos asociados.
     - `test_download_dataset_creates_zip`: simula la descarga, verifica el ZIP y la creación del registro de descarga.
     - `test_download_dataset_not_found`: comprueba respuesta 404 cuando faltan los archivos.
     - `test_compare_versions_page_renders`: comprueba la página de comparación de versiones.
     - `test_compare_version_ids_detects_changes`: valida que la comparación entre versiones detecta cambios en metadatos y películas.
   - Técnica: tests basados en `test_client` y `unittest.mock` (mocks de servicios, filesystem y cookies) para mantenerlos rápidos y aislados.

2) Pruebas de carga / integración ligera con Locust (`app/modules/movie/tests/locustfile.py`) — 1 escenario

   - Objetivo: simular usuarios reales que listan, ven y descargan datasets para verificar estabilidad y latencias.
   - Comportamientos simulados: login (CSRF), `list_all_datasets`, `list_my_datasets`, `download_dataset`, `view_dataset_detail`. El script extrae IDs desde el HTML para usar descargas reales.
   - Observaciones: útil para pruebas funcionales y carga ligera; ejecutar contra un entorno de pruebas aislado para no contaminar datos.


### Workflows Implementados

He añadido un workflow de despliegue a Render (`.github/workflows/render.yml`) siguiendo las instrucciones de la práctica. Resumen corto:

- Se dispara con push a `main`.
- En el runner instala Python 3.12, dependencias y aplica migraciones/seeders usando secrets para la BD.
- Al final llama al webhook de Render para activar el despliegue.


### Scripts Implementados

También incluyo herramientas para levantar una VM de desarrollo con la herramienta enseñada en prácticas Vagrant. De esta manera se consigue aislar lo máximo el equipo con el que se trabaja para desarrollar la aplicación en una máquina virtual:

- `Vagrantfile`: VM Ubuntu (jammy), puerto 5000 del guest expuesto en 5001 del host; provisiona con un script shell (instala Python 3.12 y Puppet) y luego ejecuta los manifests en `puppet/manifests`.
- `setup-vagrant.sh`: script de ayuda que instala VirtualBox/Vagrant (si hace falta), prepara la máquina y lanza `vagrant up`.

Nota rápida: `setup-vagrant.sh` se ejecuta en tu equipo (host) para instalar VirtualBox/Vagrant y arrancar la VM; el `Vagrantfile` define la VM y los provisioners que se ejecutarán dentro de ella.

A diferencia de las prácticas, que usa la herramienta ansible, en este caso se implementa la herrmienta **Puppet** (`puppet/manifests/default.pp`) como novedad:

- Se encarga de la instalación de paquetes (Python, MariaDB), arranque y configuración de MariaDB, creación de DB/usuario de ejemplo, creación de un venv en `/home/vagrant/venv`, instalación de dependencias, ejecución de migraciones y seeders y creación del servicio systemd `flask-app`.

Nota rápida: `puppet/manifests/default.pp` se ejecuta dentro de la VM y automatiza la configuración interna (paquetes, base de datos, venv, migraciones y servicio), dejando la máquina lista para probar la aplicación.

### Anotaciones

Junto con mi compañero Samuel Granado Oliva, hemos refactorizado el código para que todos los tipos de datasets extiendan de la clase **BaseDataset**, de tal manera que no haga falta especificar en cada dataset atributos comunes que tengan los tipos de datasets.

También hice **rediseño de la interfaz** de uvlhub a moviehub actualizando el logo de la página y los colores principales.

Por última cosa a destacar, me he encargado de realizar el contenido de algunos documentos como `Diario de equipo.md` y el `Readme.md`  principal del proyecto.

### Conclusión

He implementado la funcionalidad de "Trending datasets" en la pantalla principal (top 3 por descargas del último mes) y centralicé la lógica de autor en el servicio para mantener las rutas limpias. Paralelamente diseñé una batería de pruebas: 17 unitarias para el repositorio/servicio de descargas y 9 unitarias para las rutas/descargas de movie, un test de interfaz con Selenium y varios escenarios de carga con Locust para validar la dinámica del ranking bajo uso real.

Para facilitar reproducibilidad y despliegue añadí soporte de infraestructura: un workflow de CI/CD para Render, un Vagrantfile + setup-vagrant.sh para entornos locales y un manifest Puppet (default.pp) que deja la VM lista con ejecutar un solo script (BD, venv, migraciones, servicio systemd).

En conjunto, se consiguió entregar la funcionalidad a tiempo, cubrirla con pruebas en varios niveles y automatizar el entorno de desarrollo/despliegue con Vagrant y Render para que otros puedan replicar y validar fácilmente los cambios.


## Conclusión final

Durante este período, los integrantes de movie-hub han sabido trabajar en equipo correctamente la mayor parte del tiempo, aspecto positivo teniendo en cuenta que varios de ellos no habían trabajado previamente con los demás.

Por otra parte, aunque se ha entregado todo correctamente a tiempo, se podría haber mejorado internamente la gestión del tiempo de cada entregable, ya que sobre todo al principio se fue un poco apurado quedándose algunas issues bastante tiempo registradas sin llegar a empezarse. Sin embargo, pese a ese detalle, todo se entregó a tiempo y de forma correcta.

Finalmente, como balance general, consideramos que ha sido un buen proyecto en equipo al haber entregado todo como se había previsto desde un inicio, sin retrasos importantes y con una buena metodología de trabajo.
