# 101-setup_web_static.pp

# Ensure the web_static directory exists
file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Ensure the releases directory exists
file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure the shared directory exists
file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Ensure the test directory exists within releases
file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}

# Create a fake HTML file inside the test directory
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => '<html>\n<head>\n</head>\n<body>\n  Holberton School\n</body>\n</html>\n',
}

# Create a symbolic link to the test directory
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'root',
  group  => 'root',
  mode   => '0755',
}