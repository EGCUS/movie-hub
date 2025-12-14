<div style="text-align: center">
  <img src="app/static/img/logos/movie-hub-dark.png" alt="Logo" />
</div>

# 🎬 Movie-Hub

**Movie-Hub** es un repositorio centralizado de *datasets* de películas diseñado para facilitar análisis de datos, investigación académica y desarrollo de modelos de machine learning. El objetivo es ofrecer datos limpios, organizados y bien documentados relacionados con el mundo del cine.

---

## 🌍 Despliegue del Proyecto

Movie-Hub está disponible públicamente en dos entornos:

### 🔵 Producción (Render)
👉 **URL de producción:**  
**https://movie-hub-lvra.onrender.com**

### 🟢 Desarrollo (Railway)
👉 **URL de desarrollo:**  
**https://movie-hub-preview.up.railway.app**

---

## 🚀 Despliegue con Vagrant

Movie-Hub incluye una configuración automatizada con **Vagrant** y **Puppet** para crear un entorno de desarrollo completo y reproducible.

### 📋 Requisitos previos

- **Sistema operativo**: Linux (Ubuntu recomendado)
- **Recursos**: Al menos 2GB de RAM y 20GB de espacio en disco
- **Permisos**: Acceso sudo para instalar dependencias

### ⚡ Instalación rápida (recomendada)

Ejecuta el script automatizado que instalará todas las dependencias y levantará el entorno:
```bash
chmod +x setup-vagrant.sh
./setup-vagrant.sh
```

El script realizará automáticamente:
- ✅ Instalación de VirtualBox
- ✅ Instalación de Vagrant desde el repositorio oficial de HashiCorp
- ✅ Descarga de módulos KVM (detecta Intel/AMD automáticamente)
- ✅ Inicio de la máquina virtual
- ✅ Provisión con Puppet (base de datos, Python 3.12, dependencias, migraciones y seeders)


### 🔧 Instalación manual

Si prefieres instalarlo paso a paso:

#### 1. Instalar VirtualBox y Vagrant
```bash
# Actualizar repositorios
sudo apt update

# Instalar VirtualBox
sudo apt install -y virtualbox virtualbox-ext-pack

# Añadir repositorio de HashiCorp
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Instalar Vagrant
sudo apt update && sudo apt install vagrant
```

#### 2. Descargar módulos KVM (solo si es necesario)

Para procesadores **Intel**:
```bash
sudo modprobe -r kvm_intel
```

Para procesadores **AMD**:
```bash
sudo modprobe -r kvm_amd
```

#### 3. Iniciar la máquina virtual
```bash
vagrant up
```

### 🌐 Acceder a la aplicación

Una vez completado el despliegue, la aplicación estará disponible en:
```
http://localhost:5001
```

### 📝 Comandos útiles de Vagrant
```bash
# Conectarse a la VM
vagrant ssh

# Ver estado de la VM
vagrant status

# Detener la VM
vagrant halt

# Reiniciar la VM
vagrant reload

# Aplicar cambios de configuración sin reiniciar
vagrant provision

# Eliminar completamente la VM
vagrant destroy

# Ver los puertos mapeados
vagrant port
```

### 🔍 Verificar el estado de los servicios

Dentro de la VM, puedes verificar que todo funciona correctamente:
```bash
# Conectarse a la VM
vagrant ssh

# Verificar MariaDB
sudo systemctl status mariadb

# Verificar Flask
sudo systemctl status flask-app

# Ver logs de Flask en tiempo real
sudo journalctl -u flask-app -f

# Comprobar la base de datos
mysql -u uvlhubdb_user -puvlhubdb_password uvlhubdb -e "SHOW TABLES;"
```

### 🛠️ Configuración del entorno

El aprovisionamiento con Puppet configura automáticamente:

- **Python 3.12** instalado desde el PPA deadsnakes
- **MariaDB** con base de datos `uvlhubdb` y usuario `uvlhubdb_user`
- **Entorno virtual Python** en `/home/vagrant/venv`
- **Dependencias del proyecto** instaladas desde `requirements.txt`
- **Rosemary** instalado en modo editable
- **Migraciones de base de datos** aplicadas automáticamente
- **Seeders** ejecutados para datos de prueba
- **Servicio systemd** para Flask que arranca automáticamente

### ⚙️ Personalización

Si necesitas modificar la configuración:

- **Base de datos**: Edita las credenciales en `puppet/manifests/default.pp`
- **Puertos**: Modifica el `Vagrantfile` en la sección `forwarded_port`
- **Provisión**: Ajusta los comandos en `puppet/manifests/default.pp`

### ❗ Solución de problemas

**La aplicación no carga en el navegador:**
```bash
vagrant ssh
sudo systemctl status flask-app
sudo journalctl -u flask-app -n 50
```

**Error de módulos KVM:**
```bash
# Verificar soporte de virtualización
egrep -c '(vmx|svm)' /proc/cpuinfo
# Si devuelve 0, la virtualización no está habilitada en la BIOS
```

**Recrear el entorno desde cero:**
```bash
vagrant destroy -f
vagrant up
```


## 🐳 Despliegue con Docker

Movie-Hub también ofrece despliegue con **Docker** para entornos de producción y desarrollo, utilizando contenedores para una configuración rápida y reproducible.

### 📋 Requisitos previos

- **Docker** y **Docker Compose** instalados en tu sistema
- **Archivo de variables de entorno** `.env.docker` configurado, para ello se puede tomar el archivo `.env.docker.example` y rellenarlo de la siguiente manera para usar una base de datos autocontenida:

```
FLASK_APP_NAME="movie-hub"
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

### ⚡ Instalación rápida (producción)

Para desplegar la versión de producción (rama `main`):

```bash
# Nótese que los comandos se ejecutan desde la raíz del proyecto, para comodidad del usuario
# Traer los cambios de dockerhub
docker compose -f docker/docker-compose.yml --profile main pull
# Levantar los servicios
docker compose -f docker/docker-compose.yml --profile main up -d
```

Esto iniciará:
- ✅ Contenedor de la aplicación web (puerto 5002)
- ✅ Base de datos MariaDB
- ✅ Espera automática a que la DB esté lista
- ✅ Migraciones y seeders ejecutados

### 🟢 Instalación para preview

Para desplegar la versión de preview (rama `develop`):

```bash
# Nótese que los comandos se ejecutan desde la raíz del proyecto, para comodidad del usuario
# Traer los cambios de dockerhub
docker compose -f docker/docker-compose.yml --profile develop pull
# Levantar los servicios
docker compose -f docker/docker-compose.yml --profile develop up -d
```

Esto iniciará:
- ✅ Contenedor de la aplicación web (puerto 5003)
- ✅ Base de datos MariaDB
- ✅ Espera automática a que la DB esté lista
- ✅ Migraciones y seeders ejecutados

### 🌐 Acceder a la aplicación

- **Producción**: `http://localhost:5002`
- **Preview**: `http://localhost:5003`

### 📝 Comandos útiles de Docker

```bash
# Ver logs de los contenedores
docker logs -f <nombre_o_id_del_contenedor>

# Ver estado de los contenedores
docker ps

# Listar todos los contenedores, aunque no estén funcionando
docker ps -a

# Limpiar volúmenes, ojo: borra todo (contenedores, incluido el de la base de datos, volúmenes y networks)
docker compose -f docker/docker-compose.yml down -v
```

### 🛠️ Configuración del contenedor

El **Dockerfile** (`docker/images/Dockerfile`) configura:
- **Python 3.12** como base
- **Dependencias** instaladas desde `requirements.txt`
- **Rosemary** (CLI del proyecto) instalado
- **Scripts de inicio** para migraciones y seeders
- **Puerto 5000** expuesto

Los contenedores esperan automáticamente a que MariaDB esté disponible antes de iniciar la aplicación.