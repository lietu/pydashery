include:
    - ntp

/home/vagrant:
    file.directory:
        - user: vagrant
        - group: vagrant
        - mode: 750
        - makedirs: True
