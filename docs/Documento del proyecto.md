# movie-hub
- _Todos los integrantes pertenecen al grupo 3 de tarde_
- _Curso académico 2025/26_

## Indicadores del proyecto

- Enlace a indicadores de github: [Github insights](https://github.com/EGCUS/movie-hub/graphs/contributors)
- Enlace a zenhub (gestión de issues): [Tablero zenhub](https://github.com/egcus/movie-hub/issues#workspaces/movie-hub-69025052ce1a0b000f507adb/board)

Miembro del equipo  | Horas | Commits | LoC | Test | Issues | Work Item| Dificultad
------------- | ------------- | ------------- | ------------- | ------------- | ------------- |  ------------- |  ------------- | 
[Adame Mantecón, Manuel](https://github.com/ManuelAdame) | 50 | 8 | +601/-110 | 6 | 4 | Enviar un correo electrónico de verificación cuando un nuevo usuario se registra, para confirmar que la dirección de correo electrónico es válida | L |
[Buzón Muñoz, Manuel Zoilo](https://github.com/manumnzz) | 60 | 13 | +2159/-751 | 13 | 7 | Permite comparar versiones de un dataset para identificar qué ha cambiado entre ellas | H |
[Carmona Reina, Alejandro](https://github.com/aleecar04) | 70 | 44 | +8236/-2966 | 39 | 18 | Permitir cambios menores en los datasets que no impliquen cambios en los archivos ni en el contenido sustancial, siguiendo el modelo Zenodo. Estos cambios no generan un nuevo DOI, sino que actualizan el conjunto de datos existente | H |
[Granado Oliva, Samuel](https://github.com/SamuelGRA) | 65 | 44 | +2950/-1793 | 7 | 32 | Limitar los intentos fallidos de inicio de sesión para evitar ataques de fuerza bruta | L |
[Lavado Corredera, Manuel](https://github.com/60Manu82) | 30 | 10 | +975/-256 | 17 | 6 | Filtrado de los resultados de búsqueda por comunidad, para centrarse en conjuntos de datos de un tema o institución específicos | M |
[Román Jiménez, Darío](https://github.com/DarioRJ17) | 65 | 28 | +2324/-983 | 30 | 23 | Una clasificación de los datasets más vistos o descargados recientemente para descubrir qué es popular en la plataforma | M |
**TOTAL** | 250  | 147 | +17245/-6859 | 112 | 90 | Se han realizado 8 work items en total, 2 de cada dificultad. Además de los 2 work items obligatorios, fakenodo y newdataset | H(2)/M(2)/L(2) |

## Integración con otros equipos
No aplica (equipo single).

## Resumen ejecutivo

**Movie-Hub** es un repositorio centralizado de datasets de películas diseñado como plataforma web integral para facilitar análisis de datos, investigación académica y desarrollo de modelos de machine learning en el dominio cinematográfico. El proyecto ha sido desarrollado por un equipo de seis integrantes durante el curso académico 2025/26, implementando una arquitectura modular basada en Flask.

### Propósito y Objetivos

El objetivo fundamental del proyecto es proporcionar un sistema de gestión centralizado de datasets de películas que permita a investigadores, analistas de datos y desarrolladores acceder, compartir y colaborar en colecciones de datos cinematográficos de alta calidad. La plataforma se posiciona como un hub integrador que combina funcionalidades de repositorio de datos con herramientas de análisis y visibilidad de información.

### Funcionalidades Principales Implementadas

La plataforma Movie-Hub implementa ocho work-items de desarrollo distribuidos en tres niveles de dificultad (dos de cada nivel más dos obligatorios). Entre las características principales destacan:

**Autenticación y Seguridad:** Sistema de registro y autenticación de usuarios con funcionalidad de verificación por correo electrónico. Se incluye limitación de intentos fallidos de login para prevenir ataques de fuerza bruta, aspecto crítico en cualquier plataforma web.

**Gestión de Datasets:** Los usuarios pueden crear, subir y gestionar sus propias colecciones de películas. Cada dataset es acompañado de metadatos detallados incluyendo título, descripción, tipo de publicación y autoría. La plataforma integra con un sistema fake de Zenodo (Fakenodo) para asignar DOIs y versionar datasets.

**Sistema de Versionado:** Permite comparar diferentes versiones de un dataset para identificar cambios entre ellas. Imitando el modelo de Zenodo, soporta cambios menores en datasets que no generan nuevos DOIs sino que actualizan el conjunto existente, optimizando la gestión de versiones y metadatos.

**Búsqueda y Filtrado:** Los resultados de búsqueda pueden filtrarse por comunidad, permitiendo a usuarios centrarse en conjuntos de datos de temas o instituciones específicas, facilitando el descubrimiento contextualizado.

**Ranking y Descubrimiento:** Implementa una clasificación de datasets más vistos o descargados recientemente, permitiendo identificar contenido popular en la plataforma y facilitando el descubrimiento de recursos comunitarios.

**Gestión de Contenido:** Soporte para múltiples películas por dataset, con campos detallados incluyendo título, año, duración, país, director, productora, género, sinopsis y ratings de IMDb. Los datasets se pueden descargar completos con información consolidada sobre tamaño total.

### Arquitectura Técnica

La aplicación está construida con **Python 3.12** como lenguaje base, utilizando el framework **Flask 3.1.1** para la lógica de backend web. Se emplea **SQLAlchemy 3.1.1** como ORM para gestión de base de datos, con migraciones administradas mediante **Alembic 1.16.4**. El frontend integra **Bootstrap 5** para interfaz responsive y **Feather Icons** para iconografía consistente.

La estructura modular del proyecto organiza funcionalidades en blueprints específicos: `auth` para autenticación, `dataset` para gestión base de datos, `movie` para lógica cinematográfica, `explore` para búsqueda, `fakenodo` para integración con servicios de versionado, `featuremodel` para modelos de características, `profile` para gestión de perfiles, `team` para colaboración y `webhook` para eventos.

### Entorno de Despliegue

El proyecto implementa una configuración de infraestructura completa con **Docker** y **Docker Compose**, proporcionando múltiples configuraciones para desarrollo y producción. Se incluye automatización con **Vagrant** y **Puppet** para crear entornos reproducibles. La plataforma está desplegada en dos entornos: producción en Render (https://movie-hub-lvra.onrender.com) y desarrollo en Railway.

### Testing y Calidad

Se han implementado tests automatizados con **pytest** y análisis de carga con **Locust**, permitiendo simulación del comportamiento bajo estrés. Se incluyen linters y formatters como **Black**, **isort** y **flake8** para garantizar consistencia de código.

### Datos Disponibles

El repositorio proporciona acceso a metadatos cinematográficos detallados incluyendo títulos, años, géneros, duraciones, repartos, información de producción, ratings y datos de taquilla. Los datasets pueden ser derivados de fuentes abiertas o enriquecidos a través de APIs públicas.

### Cumplimiento de Objetivos

Durante el desarrollo, el equipo ha realizado un total de 8 work items completados (2 de cada nivel de dificultad) además de los 2 work items obligatorios (fakenodo y newdataset). La plataforma está funcional para exploración pública de datasets, gestión privada de colecciones de usuarios, y un flujo completo de versionado y publicación integrado con sistemas externos de gestión de DOIs.

### Conclusiones Iniciales

Movie-Hub representa una implementación exitosa de un repositorio centralizado de datasets con funcionalidades avanzadas de versionado, autenticación y descubrimiento. El proyecto demuestra una arquitectura escalable y modular, lista para extensión futura con funcionalidades adicionales como análisis avanzados, colaboración en tiempo real y integraciones con otras plataformas de research. 

## Descripción del sistema

### Visión General Arquitectónica

Movie-Hub implementa una arquitectura en capas modular basada en Flask, siguiendo el patrón de blueprints para organizar funcionalidades de forma independiente. El sistema se estructura en tres capas principales: presentación (templates y vistas), lógica de negocio (servicios y repositorios) y persistencia (modelos y base de datos).

### Componentes Principales del Sistema

**Módulo de Autenticación (`auth`):** Gestiona el ciclo completo de usuarios, incluyendo registro, login y perfiles. Implementa validación de contraseñas mediante hashing seguro con `werkzeug.security`, almacenamiento de credenciales en la base de datos y autenticación mediante Flask-Login. Este módulo es fundamental para garantizar que solo usuarios autenticados puedan acceder a funcionalidades protegidas.

**Módulo de Gestión de Datos (`dataset`):** Base del sistema, proporciona modelos y servicios para gestionar metadatos de datasets. Define estructuras para publicación, autores, métricas y tipos de publicación. Contiene la clase `DataSet` que representa datasets de modelos de características (UVL) con versionado completo. Incluye repositorios especializados para operaciones CRUD y servicios para cálculo de tamaños, gestión de sincronización y obtención de DOIs.

**Módulo de Películas (`movie`):** Extiende la funcionalidad base de datasets para contenido cinematográfico. Implementa dos modelos clave: `Movie` para películas individuales con campos cinematográficos (título, año, director, género, ratings de IMDb, sinopsis) y `MovieDataset` que agrupa múltiples películas. Proporciona servicios especializados para operaciones específicas de datasets de películas y gestión de cambios menores sin generación de nuevas versiones.

**Modelo de Versionado:** Implementa un sistema completo de control de versiones inspirado en Zenodo. Cada dataset puede tener múltiples versiones identificadas por números (1.0, 2.0, etc.). Las versiones capturan snapshots JSON del estado completo del dataset incluyendo metadatos, películas y autores. El sistema permite comparar versiones para identificar cambios específicos.

**Sistema de Cambios Menores (`DatasetChangeLog`):** Uno de los cambios más significativos del proyecto, permite registrar cambios menores en metadatos (título, descripción, autores, tags) sin generar nuevas versiones o DOIs. Cada cambio registra el tipo de modificación, usuario responsable, timestamp y comentario opcional. Esto sigue el modelo de Zenodo donde cambios cosméticos no requieren nuevo DOI.

**Módulo Fakenodo (`fakenodo`):** Implementa una versión simulada del sistema de Zenodo para desarrollo. Asigna DOIs ficticios a datasets en formato `10.1234/moviehub.fake.{uuid}` y gestiona estados de publicación. Cuando se publica un dataset, se crea un registro Fakenodo que almacena la información del DOI y metadatos asociados. Este módulo permite desarrollo y testing sin dependencias externas.

**Módulo de Modelos de Características (`featuremodel`):** Gestiona datos de modelos de características (UVL) que pueden asociarse a datasets de películas. Cada modelo de característica tiene metadatos detallados y métricas. Los archivos se almacenan en estructura jerárquica por usuario y dataset.

**Módulo de Búsqueda y Exploración (`explore`):** Proporciona capacidades de búsqueda, filtrado y descubrimiento de datasets. Implementa filtrado por comunidades/tags y ranking de datasets populares basado en vistas y descargas.

### Flujo de Datos y Relaciones

El sistema maneja dos tipos principales de datos: **metadatos** (información descriptiva de datasets) y **contenido** (películas, archivos de características). Los metadatos se centralizan en `DSMetaData` que incluye título, descripción, autores y tipos de publicación. Cada dataset mantiene relación con su owner (`user_id`), asegurando que solo propietarios puedan modificar datasets.

Las películas se almacenan como entidades independientes relacionadas con `MovieDataset` mediante foreign key. Cada película contiene campos extensivos: información básica (título, año, duración), equipo creativo (director, productora), clasificación (género, sinopsis) y datos de IMDb (rating, votos). Los datos se serializan a JSON en varios puntos para APIs y exportación.

### Gestión de Versiones y Cambios

El versionado funciona en dos niveles: **versiones mayores** que generan nuevos DOIs (cambios sustanciales) y **cambios menores** que se registran en changelog (modificaciones cosméticas). Cuando se crea una versión, el sistema genera un snapshot JSON en la estructura `uploads/user_{id}/dataset_{id}/versions/{version_id}`.

La comparación de versiones implementa lógica para detectar:
- Cambios en metadatos (campos que difieren entre versiones)
- Películas añadidas/eliminadas/modificadas
- Cambios en autores y tags

El changelog captura modificaciones de usuario en formato JSON, permitiendo auditoría completa de quién cambió qué y cuándo.

### Cambios Desarrollados para el Proyecto

Durante el desarrollo del curso, se implementaron ocho work items de desarrollo específicos con dificultad variada, 2 de dificultad baja, 2 de dificultad media y otros dos de dificultad alta, teniendo en cuenta además los 2 work items obligatorios que se debían realizar:

1. **Verificación por Correo Electrónico (Dificultad Baja):** Sistema automático que envía correos de verificación cuando usuarios se registran, confirmando validez del email mediante tokens únicos.

2. **Limitación de Intentos de Login (Dificultad Baja):** Protección contra ataques de fuerza bruta limitando intentos de autenticación fallidos con bloqueos temporales.

3. **Sistema de Filtrado por Comunidad (Dificultad Media):** Implementación de búsqueda avanzada permitiendo filtrar datasets por tags/comunidades específicas, mejorando descubrimiento contextualizado.

4. **Ranking de Datasets Populares (Dificultad Media):** Clasificación de datasets por vistas y descargas recientes, facilitando identificación de contenido popular en la plataforma.

5. **Comparación de Versiones (Dificultad Alta):** Interfaz visual completa para comparar dos versiones de dataset, mostrando metadatos modificados, películas añadidas/eliminadas, permitiendo así un análisis detallado de la evolución del dataset.

6. **Edición de Metadatos sin Nuevo DOI (Dificultad Alta):** Sistema de cambios menores imitando el modelo de Zenodo. Permite actualizar títulos, descripciones, autores sin generar nuevas versiones ni DOIs, con auditoría completa en changelog.

7. **Fakenodo (Work Item Obligatorio):** Integración con sistema simulado de Zenodo para asignación de DOIs, publicación de datasets y gestión de versiones con persistencia de información.

8. **NewDataset (Work Item Obligatorio):** Reestructuración arquitectónica para desvincular la plataforma de un único tipo de dataset (UVL) y convertirla en un hub genérico de tipos de datos (`[datatype]hub`), moviehub en nuestro caso. 

### Persistencia de Datos

Los datos se almacenan en PostgreSQL con migraciones administradas por Alembic. La estructura de tablas utiliza herencia de SQLAlchemy mediante tabla polimórfica: `base_dataset` contiene información común, con `data_set` y `movie_dataset` como especializaciones. Los archivos se almacenan en estructura de carpetas `uploads/user_{id}/dataset_{id}/` con versionado en subcarpetas.

### Integración de Subsistemas

El sistema integra múltiples subsistemas externos: PostgreSQL para persistencia, Flask-Mail para notificaciones por correo, Bootstrap/Feather Icons para UI, y Locust para testing de carga. La arquitectura permite que los subsistemas sean reemplazables mediante inyección de dependencias en servicios. 


## Visión global del proceso de desarrollo

#### Flujo integral: de idea a producción

El desarrollo de Movie‑Hub sigue un ciclo iterativo basado en git, GitHub Issues, Zenhub y GitHub Actions (workflows CI/CD). El proceso garantiza trazabilidad, revisión de cambios y calidad mediante automatización.

**Fases del ciclo:**

1. **Planificación (GitHub Issues + Zenhub)**: un requisito (feature, documentación, pruebas o bug fixing) se añade al tablero Zenhub, lo que a su vez crea automáticamente una issue de GitHub. La issue se etiqueta según su tipo, se añade a su milestone correspondiente y se asigna a un desarrollador. Si la tarea es una feature que requiere pruebas, estas se gestionarán en una issue separada.

2. **Ramificación (Git)**: Antes de empezar a trabajar sobre la issue, el desarrollador debe moverla a la columna `In progress` para dejar constancia al resto del equipo de que la tarea ya se está llevando a cabo. Tras eso el desarrollador crea una rama local desde `develop` siguiendo la convención `<tipo-de-issue>/descripcion-corta`. Ejemplo: `feature/add-movie-ratings-export`.

3. **Implementación (local + tests)**: en la rama local se escribe código, y al terminar se hace commit y push de los mismos. Los cambios se hacen en pequeños commits con mensajes claros.

4. **Push y Pull Request (GitHub)**: cuando el cambio está listo, se hace push a la rama remota. Los workflows se encargarán de comprobar que los cambios introducidos por la rama no producen conflictos en la rama `develop`y que los tests siguen funcionando correctamente. Si es así se fusiona la rama remota con `develop`y esa rama remota es automáticamente eliminada, porque ya no tiene utilidad alguna. Una vez el código está integrado en develop, el desarrollador debe mover la issue a la columna `Done`en ZenHub.

5. **Revisión y CI/CD (GitHub Actions)**: Si los workflows detectan algún problema, el desarrollador ajusta el código creando una rama de tipo `fix`y volvería a seguirse el flujo de los puntos 2 a 5. Cuando todo funcione correctamente, los workflows fusionarán la rama remota y todo quedará integrado en `develop`.

6. **Despliegue a staging (Railway)**: los cambios en `develop` disparan un workflow que despliega automáticamente a ambiente de desarrollo (Railway). El equipo prueba funcionalidad en staging.

7. **Despliegue a producción (Render)**: Tras realizar una release (en nuestro equipo esto es equivalente a fusionar las ramas `develop` y `main`) se ejcuta un workflow que despliega el código que haya en la rama main en Render. También hay un workflow que sube el código a Codacy para probar la calidad de este. Además con cada nueva release se sube una nueva imagen del proyecto a DockerHub.

8. **Versiones y changelog**: Al hacer una release se activa un workflow que recoge los mensajes de commit escritos por los desarrolladores y en base al tipo de rama/issue (feature, fix...) genera una nueva etiqueta con la versión del proyecto. Además generará una release de GitHub que incluirá los mensajes de commit de los desarrolladores, a modo de changelog.

### Entorno de desarrollo

#### Resumen del entorno

Durante el desarrollo de Movie‑Hub el equipo trabajó principalmente sobre sistemas Linux (Ubuntu recomendado) y empleó Python 3.12 como intérprete estándar. La aplicación está construida sobre Flask 3.1.1 y utiliza dependencias clave que aparecen en `requirements.txt`, destacando SQLAlchemy 3.1.1 para el acceso a datos y Alembic 1.16.4 para migraciones. Para ofrecer un flujo de trabajo reproducible se proporcionan tres vías de instalación: (A) VM reproducible con `Vagrant` + `Puppet`, (B) contenedores con `Docker` + `docker‑compose` y (C) instalación local con `venv`/virtualenv. Cada opción cubre necesidades distintas (homogeneidad, rapidez o simplicidad) y está documentada en el repositorio.

#### Herramientas y versiones principales

- **SO:** Linux (Ubuntu recomendado)
- **Python:** 3.12
- **Framework:** Flask 3.1.1
- **ORM:** SQLAlchemy 3.1.1
- **Migraciones:** Alembic 1.16.4 (Flask‑Migrate)
- **Base de datos:** PostgreSQL (13+ recomendada)
- **Contenedores:** Docker & Docker Compose
- **Provisionamiento:** Vagrant + Puppet (script `setup-vagrant.sh` incluido)
- **Testing:** pytest; Locust para pruebas de carga
- **Calidad:** Black, isort, flake8

#### Instalación y puesta en marcha (opciones)

Opción A — Vagrant + Puppet (entorno reproducible, recomendado para desarrollo homogéneo):

1. Instalar VirtualBox y Vagrant en la máquina host.
2. Ejecutar el script de configuración incluido:

```bash
chmod +x setup-vagrant.sh
./setup-vagrant.sh
vagrant ssh
```

Dentro de la VM provisionada, Puppet instala Python 3.12, PostgreSQL, dependencias y aplica migraciones y seeders. Tras la provisión la aplicación estará disponible en `http://localhost:5001` según la configuración de red.

Opción B — Docker + docker-compose (rápido y portable):

Movie-Hub también ofrece despliegue con **Docker** para entornos de producción y desarrollo, utilizando contenedores para una configuración rápida y reproducible.

Hay dos cosas que se deben hacer antes de desplegar el contenedor de docker
- **Docker** y **Docker Compose** instalados en tu sistema
- **Archivo de variables de entorno** `.env.docker` configurado, para ello se puede tomar el archivo `.env.docker.example` y rellenarlo de la siguiente manera para usar una base de datos autocontenida:

```
FLASK_ENV=development
MARIADB_HOSTNAME=db
MARIADB_PORT=3306
MARIADB_DATABASE=uvlhubdb
MARIADB_TEST_DATABASE=uvlhubdb_test
MARIADB_USER=uvlhubdb_user
MARIADB_PASSWORD=uvlhubdb_password
MARIADB_ROOT_PASSWORD=uvlhubdb_root_password
WORKING_DIR=/app
```

Para desplegar la versión de producción (rama `main`):
```bash
# Traer los cambios de dockerhub
docker compose -f docker/docker-compose.yml --profile main pull
# Levantar los servicios con el perfil main
docker compose -f docker/docker-compose.yml --profile main up -d
```

Para desplegar la versión de preview (rama `develop`):
```bash
# Traer los cambios de dockerhub
docker compose -f docker/docker-compose.yml --profile develop pull
# Levantar los servicios con el perfil develop
docker compose -f docker-compose.yml --profile develop up -d
```

Para acceder a la aplicación, dependiendo de qué contenedor esté desplegado:
- **Producción**: `http://localhost:5002`
- **Preview**: `http://localhost:5003`

Para limpiarlo todo se puede ejecutar lo siguiente:
```bash
docker compose -f docker/docker-compose.yml down -v
```
Eso eliminará todos los contenedores, volúmenes y networks relacionados con movie-hub de la máquina local.

Opción C — Local con entorno virtual (para desarrollo directo):

1. Clonar el repositorio

```bash
git clone https://github.com/EGCUS/movie-hub.git
cd movie-hub
```

2. Crear y activar un entorno virtual con Python 3.12:

```bash
sudo apt install python3.12-venv # Si no se tiene ya
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ./
```

3. Definir variables de entorno mínimas, basta con copiar el archivo `.env.local.example` a un archivo llamado `.env`:
```bash
cp .env.local.example .env
```

4. Crear la base de datos y aplicar migraciones:

```bash
sudo apt install mariadb-server -y
sudo systemctl start mariadb
sudo mysql_secure_installation
# Aquí se hacen una serie de preguntas, se puede responder con 'y' a todas, es importante recordar la contraseña que se establezca, porque se pedirá cada vez que se ejecute el siguiente comando
sudo mysql -u root -p
CREATE DATABASE uvlhubdb;
CREATE DATABASE uvlhubdb_test;
CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
echo "webhook" > .moduleignore
flask db upgrade
# (Recomendable) Ejecutar seeders: rosemary db:seed
```

5. Ejecutar la aplicación:

```bash
flask run --host=0.0.0.0 --reload
# La aplicación debería estar disponible en http://localhost:5000 si todo ha ido bien
```

#### Variables de entorno y configuración

Variables relevantes:

- `DATABASE_URL` (cadena de conexión a PostgreSQL)
- `SECRET_KEY` (clave de Flask)
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` (para `Flask‑Mail`)
- `WORKING_DIR` (raíz del repo usada por `BaseBlueprint` para localizar módulos y assets)

Se recomienda usar un `.env` para desarrollo local o inyectar variables desde la provisión de Vagrant/Docker.

#### Pruebas y análisis

- Ejecutar tests unitarios:

```bash
pytest -v
```

- Pruebas de carga básicas con Locust (locustfile incluido):

```bash
locust -f app/modules/movie/tests/locustfile.py
# Cambiando movie por el módulo que se quiera probar, se puede acceder a la interfaz de locust en http://0.0.0.0:8089
```


#### Diferencias entre miembros del equipo

El equipo empleó estrategias distintas según preferencias y necesidades: algunos usaron la VM provisionada con Vagrant para reproducir exactamente el entorno del proyecto; otros optaron por Docker por su rapidez y portabilidad; y otros trabajaron localmente con `venv`. Para evitar problemas se incluyeron scripts y ficheros de configuración para soportar los tres flujos.

#### Recomendaciones finales

1. Para clonar y empezar rápidamente, usar `setup-vagrant.sh` garantiza reproducibilidad.
2. Mantener `requirements.txt` sincronizado tras cambios en dependencias.
3. Para despliegue en producción usar imágenes y el `docker-compose.prod.yml` o plataformas gestionadas (Render/Railway) con variables de entorno seguras.


### Ejercicio de propuesta de cambio

#### Ejemplo concreto: agregar exportación de películas en CSV

Imaginemos que se requiere poder descargar un dataset de películas en formato CSV (además de JSON).

**Paso 1: Issue y planificación**
- Se crea Issue `Añadir exportación como CSV a datasets de películas` en ZenHub.
- Se etiqueta como `feature`.
- Se añade al Milestone o Sprint actual en Zenhub.
- Se asigna al desarrollador X.
- Se mueve la issue a la columna `To do` una vez esté asignada.

**Paso 2: Rama local**
Antes de empezar a trabajar en la Isuue, el desarrollador la debe mover a la columna `In progress` en ZenHub.
```bash
# Estando en la rama develop, si no se está en ella: git checkout develop
git pull
git checkout -b feature/movie-csv-export
```

**Paso 3: Implementación**
El desarrollador implementaría los cambios correspondientes y al terminar los subiría a GitHub. Si fuera necesario, en una rama `test/testing-movie-csv-export` se escribirían las pruebas, pero eso iría asociado a una issue independiente como se explicó antes:

```bash
#Recomendable ejecutar los tests del módulo modificado para comprobar que el nuevo código no rompe nada, aunque igualmente los workflows los ejecutarán
pytest app/modules/movie/tests/test_export.py -v
```

**Paso 4: Push y Pull Request**
```bash
git add .
git commit -m "feat: add CSV export for movie datasets"
git push -u origin feature/movie-csv-export
```

Los workflows se encargarán de todo lo demás, comprobarán que los cambios son válidos e integrarán el nuevo código en la rama `develop`. Tras eso, el desarrollador puede mover su issue de ZenHub a la columna `Done`.

**Paso 5: Revisión y CI/CD**
- GitHub Actions ejecuta: pytest (pasa), y comprueba que no haya conflictos entre ramas.
- Si todo va bien, se mergea a `develop` y se borra la rama remota.

**Paso 6: Staging (Railway)**
- Automáticamente se despliega a `https://movie-hub-preview.up.railway.app`.

**Paso 7: Producción (Render)**
Cabe destacar que esto solo ocurre cuando se hace una release, cosa que no se suele hacer para un cambio minoritario, pero imaginemos que creamos una release solo para este cambio.
```bash
#Si no se está en la rama main: git checkout main
git pull
git merge develop
git add .
git commit -m "chore(release): New release for csv export"
git push
```
Tras eso, de forma automática:
- Se ejecuta el workflow de despliegue a render, que desplegaría el código de la rama main en `https://movie-hub-lvra.onrender.com`.
- Se ejecuta el workflow de codacy, que sube el código a la plataforma para medir la calidad.

**Paso 8: Versiones y changelog**
Como consecuencia de la release realizada en el paso anterior:
- Se ejecuta el workflow de semantic versioning y release:
    - El primero de ellos generaría una nueva etiqueta tipo `v1.1.0` si la anterior fuera `v1.0.0`.
    - El segundo generaría una release de github con un texto de esta forma:
    ```
    1.1.0 (fecha de release)
    Features
    · add CSV export for movie datasets
    Bug fixes
    - ...
    ```

#### Herramientas clave en el flujo

- **Git**: control de versiones, ramas y merges.
- **GitHub**: hosting, Actions (CI/CD).
- **Zenhub**: Issues, priorización, etiquetas de dificultad.
- **pytest**: tests automatizados, cobertura.
- **Docker/Railway/Render**: contenedores, despliegue en staging y producción.
- **GitHub Actions workflows**: automatización de tests, cobertura, despliegues, etc.

Este ciclo asegura que cada cambio sea probado, revisado y trazable antes de llegar a producción.

### Conclusiones y trabajo futuro

Movie‑Hub entrega una base funcional y extensible para la gestión de datasets en el dominio cinematográfico: autenticación segura, control de versiones, registro de cambios menores y un flujo de publicación (Fakenodo) diseñado para pruebas y desarrollo. La separación por módulos (`auth`, `dataset`, `movie`, `fakenodo`, `featuremodel`, `explore`) y el uso de `BaseDataset` como núcleo facilitan la evolución hacia un ecosistema multi‑dominio sin necesidad de reescribir la plataforma.

Prioridades recomendadas para el siguiente curso:

- **Mejoras en la experiencia de subida y edición**: validaciones client/server, previsualización de CSV, subida por lotes y progreso asíncrono para archivos grandes.
- **Pipelines de enriquecimiento**: añadir procesos ETL para normalizar y enriquecer metadatos (entidades, géneros, enlaces a IMDB/API externas).
- **Observabilidad y escalado**: instrumentar métricas, logging estructurado y preparar despliegue en entornos orquestados (Kubernetes) cuando la carga lo requiera.
