#!/bin/bash

set -euo pipefail

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

cd $HOME
backup_dir="$HOME/www/python/src_backup_$(date +%Y%m%d_%H%M%S)"

# Backup existing source if it exists
if [ -d "$HOME/www/python/src" ]; then
    mv "$HOME/www/python/src" "$backup_dir" || exit 1
else
    echo "No existing source found in $HOME/www/python"
    exit 1
fi

REPO_URL="https://github.com/WikiAr/make2-web.git"

if ! git clone --branch "$BRANCH" "$REPO_URL" "$HOME/www/python/src"; then
    echo "Failed to clone repository" >&2
    if [ -d "$backup_dir" ]; then
        mv "$backup_dir" "$HOME/www/python/src"
    fi
    exit 1
fi

# Activate virtual environment with error handling

if source "$HOME/www/python/venv/bin/activate"; then
    pip install -r $HOME/www/python/src/requirements.txt
    # exit 1
else
    echo "Failed to activate virtual environment" >&2
fi

# webservice python3.11 restart

# toolforge-jobs run updatex --image python3.11 --command "$HOME/web_sh/update.sh update"
