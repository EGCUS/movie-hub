#!/bin/bash

# Script de instalación y configuración de Vagrant para el proyecto
# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Iniciando configuración de Vagrant ===${NC}\n"

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para manejar errores
handle_error() {
    echo -e "${RED}Error: $1${NC}"
    exit 1
}

# 1. Verificar si se está ejecutando como root para ciertas operaciones
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Advertencia: No ejecutes este script como root directamente.${NC}"
    echo -e "${YELLOW}El script pedirá permisos sudo cuando sea necesario.${NC}"
    exit 1
fi

# 2. Actualizar repositorios
echo -e "${GREEN}[1/5] Actualizando repositorios...${NC}"
sudo apt update || handle_error "No se pudo actualizar los repositorios"

# 3. Instalar VirtualBox
echo -e "\n${GREEN}[2/5] Instalando VirtualBox...${NC}"
if command_exists virtualbox; then
    echo -e "${YELLOW}VirtualBox ya está instalado. Versión:${NC}"
    virtualbox --help | head -n 1
else
    sudo apt install -y virtualbox virtualbox-ext-pack || handle_error "No se pudo instalar VirtualBox"
    echo -e "${GREEN}✓ VirtualBox instalado correctamente${NC}"
fi

# 4. Instalar Vagrant desde el repositorio oficial de HashiCorp
echo -e "\n${GREEN}[3/5] Instalando Vagrant...${NC}"
if command_exists vagrant; then
    echo -e "${YELLOW}Vagrant ya está instalado. Versión:${NC}"
    vagrant --version
else
    echo -e "${YELLOW}Añadiendo repositorio oficial de HashiCorp...${NC}"
    # Añadir clave GPG de HashiCorp
    wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg || handle_error "No se pudo descargar la clave GPG de HashiCorp"
    
    # Añadir repositorio de HashiCorp
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list || handle_error "No se pudo añadir el repositorio de HashiCorp"
    
    # Actualizar repositorios e instalar Vagrant
    sudo apt update || handle_error "No se pudieron actualizar los repositorios"
    sudo apt install -y vagrant || handle_error "No se pudo instalar Vagrant"
    
    echo -e "${GREEN}✓ Vagrant instalado correctamente${NC}"
    vagrant --version
fi

# 5. Descargar módulos KVM (según el tipo de procesador)
echo -e "\n${GREEN}[4/5] Descargando módulos KVM...${NC}"

# Detectar el tipo de procesador
if grep -q "Intel" /proc/cpuinfo; then
    echo -e "${YELLOW}Procesador Intel detectado${NC}"
    if lsmod | grep -q kvm_intel; then
        sudo modprobe -r kvm_intel || echo -e "${YELLOW}Advertencia: No se pudo descargar kvm_intel${NC}"
        echo -e "${GREEN}✓ Módulo kvm_intel descargado${NC}"
    else
        echo -e "${YELLOW}El módulo kvm_intel no estaba cargado${NC}"
    fi
elif grep -q "AMD" /proc/cpuinfo; then
    echo -e "${YELLOW}Procesador AMD detectado${NC}"
    if lsmod | grep -q kvm_amd; then
        sudo modprobe -r kvm_amd || echo -e "${YELLOW}Advertencia: No se pudo descargar kvm_amd${NC}"
        echo -e "${GREEN}✓ Módulo kvm_amd descargado${NC}"
    else
        echo -e "${YELLOW}El módulo kvm_amd no estaba cargado${NC}"
    fi
else
    echo -e "${YELLOW}No se pudo detectar el tipo de procesador. Saltando descarga de módulos KVM...${NC}"
fi

# 6. Verificar que existe el Vagrantfile
if [ ! -f "Vagrantfile" ]; then
    handle_error "No se encuentra el archivo Vagrantfile en el directorio actual"
fi

# 7. Iniciar Vagrant
echo -e "\n${GREEN}[5/5] Iniciando máquina virtual con Vagrant...${NC}"
echo -e "${YELLOW}Esto puede tardar varios minutos la primera vez...${NC}\n"

vagrant up || handle_error "No se pudo iniciar la máquina virtual"

# 8. Mostrar información final
echo -e "\n${GREEN}=== ¡Configuración completada! ===${NC}\n"
echo -e "${GREEN}La aplicación debería estar corriendo en:${NC} http://localhost:5000"
echo -e "\n${YELLOW}Comandos útiles:${NC}"
echo -e "  ${GREEN}vagrant ssh${NC}         - Conectarse a la VM"
echo -e "  ${GREEN}vagrant halt${NC}        - Apagar la VM"
echo -e "  ${GREEN}vagrant destroy${NC}     - Eliminar la VM"
echo -e "  ${GREEN}vagrant provision${NC}   - Re-ejecutar la configuración"
echo -e "  ${GREEN}vagrant reload${NC}      - Reiniciar la VM"
echo -e "\n${GREEN}Estado actual de la VM:${NC}"
vagrant status

echo -e "\n${GREEN}¡Todo listo!${NC}"