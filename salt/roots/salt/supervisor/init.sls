supervisor:
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: supervisor
