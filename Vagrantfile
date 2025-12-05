Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.network "forwarded_port", guest: 5000, host: 5001

  # 1) Instalar Python 3.12 y Puppet
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt install -y software-properties-common
    add-apt-repository -y ppa:deadsnakes/ppa
    apt update
    apt install -y python3.12 python3.12-venv python3.12-dev python3-pip puppet
    # Crear enlace simbólico para que python3 apunte a python3.12
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
    update-alternatives --set python3 /usr/bin/python3.12
  SHELL

  # 2) Ejecutar tus manifests Puppet
  config.vm.provision "puppet" do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file  = "default.pp"
  end
end