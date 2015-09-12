{% for pkg in 'python-setuptools', 'python-dev', 'python-pip', 'virtualenvwrapper' %}
{{ pkg }}:
    pkg.installed
{% endfor %}

pip:
    pip.installed:
    - name: pip >= 1.4.0
    - upgrade: True
    - require:
        - pkg: python-pip
