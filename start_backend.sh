#!/usr/bin/env bash

# Source a file if it exists
source_if_exists() {
    local path="$1"
    if [[ -f "$path" ]]; then
        source "$path"
    fi
}

cd "$(dirname $0)"

export HOME="/home/pi/"
source_if_exists "/etc/bash.bashrc"
source_if_exists "~/.bashrc"
source_if_exists "~/.bash_profile"
source_if_exists "/etc/bash_completion.d/virtualenvwrapper"

# Activate virtualenv
workon pydashery

# Go to correct directory
cd backend

# Launch app, replace shell so signals get passed correctly etc.
exec python -m pydashery
