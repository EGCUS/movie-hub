# --- Paquetes del sistema ---
package { [
    'python3',
    'python3-pip',
    'python3-venv',
    'mariadb-server',
    'mariadb-client'
  ]:
  ensure => present,
}

# --- Servicio de MariaDB ---
service { 'mariadb':
  ensure  => running,
  enable  => true,
  require => Package['mariadb-server'],
}

# --- Crear base de datos ---
exec { 'create-database':
  command => "mysql -u root -e \"CREATE DATABASE IF NOT EXISTS uvlhubdb;\"",
  unless  => "mysql -u root -e \"SHOW DATABASES LIKE 'uvlhubdb';\" | grep uvlhubdb",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Service['mariadb'],
}

# --- Crear usuario y permisos ---
exec { 'create-user':
  command => "mysql -u root -e \"CREATE USER IF NOT EXISTS 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password'; GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost'; FLUSH PRIVILEGES;\"",
  unless  => "mysql -u root -e \"SELECT User FROM mysql.user WHERE User='uvlhubdb_user';\" | grep uvlhubdb_user",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Exec['create-database'],
}

# --- Crear entorno virtual ---
exec { 'create-venv':
  command => "python3 -m venv /home/vagrant/venv",
  creates => "/home/vagrant/venv/bin/activate",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Package['python3-venv'],
}

# --- Instalar dependencias Python ---
exec { 'install-python-deps':
  command => "/home/vagrant/venv/bin/pip install -r /vagrant/requirements.txt",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Exec['create-venv'],
}

# --- Instalar Rosemary en modo editable ---
exec { 'install-rosemary':
  command => "/home/vagrant/venv/bin/pip install -e /vagrant/",
  cwd     => "/vagrant",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Exec['install-python-deps'],
}

# --- Migraciones (si la app Flask las usa) ---
exec { 'run-migrations':
  command => "/home/vagrant/venv/bin/flask --app app db upgrade",
  cwd     => "/vagrant",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Exec['install-rosemary'],
}

# --- Ejecutar seeders ---
exec { 'run-seeders':
  command => "/home/vagrant/venv/bin/rosemary db:seed",
  cwd     => "/vagrant",
  path    => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  require => Exec['run-migrations'],
}

# --- Crear archivo de servicio systemd para Flask ---
file { '/etc/systemd/system/flask-app.service':
  ensure  => file,
  content => "[Unit]
Description=Flask Application
After=network.target mariadb.service

[Service]
User=vagrant
WorkingDirectory=/vagrant
Environment=\"PATH=/home/vagrant/venv/bin\"
ExecStart=/home/vagrant/venv/bin/flask --app app run --host=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
",
  require => Exec['run-seeders'],
  notify  => Exec['systemd-reload'],
}

# --- Recargar systemd ---
exec { 'systemd-reload':
  command     => "systemctl daemon-reload",
  path        => ['/usr/bin', '/usr/sbin', '/bin', '/sbin'],
  refreshonly => true,
}

# --- Habilitar y arrancar el servicio Flask ---
service { 'flask-app':
  ensure  => running,
  enable  => true,
  require => [File['/etc/systemd/system/flask-app.service'], Exec['systemd-reload']],
}